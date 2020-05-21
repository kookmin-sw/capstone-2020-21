import datetime
from dateutil.parser import parse
from django.db.models import Avg, Max, Min
from django.utils import timezone
from filters.mixins import FiltersMixin
import json
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from statistics import mode

from .exceptions import S3FileError
from .globalweather import get_global_weather_city_name
from .models import Clothes, ClothesSet, ClothesSetReview, User, Weather
from .permissions import UserPermissions
from .serializers import (
    ClothesSerializer,
    ClothesSetSerializer,
    ClothesSetReadSerializer,
    ClothesSetReviewSerializer,
    ClothesSetReviewReadSerializer,
    UserSerializer
)
from .utils import *
from .validations import (
    user_query_schema, 
    clothes_query_schema, 
    clothes_set_query_schema, 
    clothes_set_review_query_schema
)
from .weather import (
    convert_time,
    get_weather_date, 
    get_weather_between, 
    get_weather_time_date, 
    get_current_weather
)

class UserView(FiltersMixin, NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    # Apply ordering, uses `ordering` query parameter.
    filter_backends = (filters.OrderingFilter, )
    ordering_fields = ('id', 'date_joined', )
    ordering = ('id', )
    
    # Apply filtering, using other query parameters.
    filter_mappings = {
        'gender': 'gender',
        'min_age': 'birthday__lte',
        'max_age': 'birthday__gte',
    }
    
    # TODO(mskwon1) : change this to a more reasonable calculation.
    filter_value_transformations = {
        'min_age' : lambda val: timezone.now() - datetime.timedelta(days=int(val)*365),
        'max_age' : lambda val: timezone.now() - datetime.timedelta(days=int(val)*365),
    }
    
    # Use filter validation.
    filter_validation_schema = user_query_schema
    
    # Permissions.
    permission_classes = [UserPermissions]

    def update(self, request, *args, **kwargs):
        user = request.user
        if user.id != int(kwargs.pop('pk')):
            return Response({
                'error' : 'you are not allowed to access this object'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user.id != int(kwargs.pop('pk')):
            return Response({
                'error' : 'you are not allowed to access this object'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def me(self, request, *args, **kwargs):
        """
        A endpoint where current user's data is returned,
        uses Authorization JWT token to check the user.
        """
        if self.request.user.is_authenticated:
            self.kwargs.update(pk=request.user.id)
            return self.retrieve(request, *args, **kwargs)
        else:
            return Response(
                {'error': 'please log in'},
                status=status.HTTP_401_UNAUTHORIZED)


class ClothesView(FiltersMixin, NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Clothes.objects.all()
    serializer_class = ClothesSerializer
    
    def get_queryset(self):
        queryset = Clothes.objects.all()
        
        # me 파라미터가 true인 경우, 해당 유저의 옷만 반환.
        if self.request.query_params.get('me'):
            user = self.request.user
            queryset = queryset.filter(owner=user.id)
                
        return queryset

    # Apply ordering, uses `ordering` query parameter.
    filter_backends = (filters.OrderingFilter, )
    ordering_fields = ('created_at', 'id', )
    ordering = ('-created_at', )

    # Apply filtering, using other query parameters.
    filter_mappings = {
        'upper_category': 'upper_category__in',
        'lower_category': 'lower_category__in',
    }
    
    filter_value_transformations = {
        'upper_category': lambda val: val.split(','),
        'lower_category': lambda val: val.split(',')
    }

    # Use filter validation.
    filter_validation_schema = clothes_query_schema
    
    # Permissions.
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def list(self, request, *args, **kwargs):
        # If me parameter is set, check authentication.
        if request.query_params.get('me') and not request.user.is_authenticated:
            return Response({
                'error': 'token authorization failed ... please log in'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        # Move image from temp to saved on s3 storage.
        # TODO(mskwon1): data 타입이 json이 아닐 경우 바꿔줘야함.
        # request.data._mutable = True
        if 'image_url' in request.data.keys():
            image_url = request.data['image_url']
            try:
                request.data['image_url']  = move_image_to_saved(image_url, 'clothes')
            except S3FileError:
                return Response({
                    'error': 'image does not exist ... plesase try again'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return super(ClothesView, self).create(request, *args, **kwargs)  
    
    def perform_create(self, serializer):
        serializer.save(owner_id = self.request.user.id)      

    def update(self, request, *args, **kwargs):
        user = request.user
        key = int(kwargs.pop('pk'))
        target_clothes = Clothes.objects.filter(id=key)
        
        if user.id != int(target_clothes[0].owner.id):
            return Response({
                'error' : 'you are not allowed to access this object'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        user = request.user
        key = int(kwargs.pop('pk'))
        target_clothes = Clothes.objects.filter(id=key)
        
        if user.id != int(target_clothes[0].owner.id):
            return Response({
                'error' : 'you are not allowed to access this object'
            }, status=status.HTTP_401_UNAUTHORIZED)
   
        return super().destroy(request, *args, **kwargs)
 
    @action(detail=False, methods=['post'])
    def inference(self, request, *args, **kwargs):
        """
        An endpoint where the analysis of a clothes is returned
        """
        image = byte_to_image(request.data['image'])
        image_tensor = image_to_tensor(image)
        inference_result = execute_inference(image_tensor)
        upper, lower = get_categories_from_predictions(inference_result)
        
        image = remove_background(image)
        image_url = save_image_s3(image, 'clothes')
        
        return Response({'image_url': image_url, 
                         'upper_category':upper, 
                         'lower_category':lower}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def today_category(self, request, *args, **kwargs):
        """
        An endpoint where the today_category is returned
        """

        min_sensible = float(request.query_params.get('min_sensible_temp'))
        max_sensible = float(request.query_params.get('max_sensible_temp'))
        
        cody_review_set = ClothesSetReview.objects.all()
        filtered_cody_review_set = cody_review_set.filter(review=3, 
                                                        min_sensible_temp__gte=min_sensible-2,
                                                        min_sensible_temp__lte=min_sensible+2, 
                                                        max_sensible_temp__gte=max_sensible-2,
                                                        max_sensible_temp__lte=max_sensible+2
                                                        )
        
        # TODO : 효빈이 serializer 공부용 -효빈-
        # serializer = ClothesSetReviewReadSerializer(filtered_cody_review_set, many=True)
        # return Response(serializer.data)    

        filtered_clothes_set_id = []
        for filtered_cody_review in filtered_cody_review_set:
            filtered_clothes_set_id.append(filtered_cody_review.clothes_set.id)
        
        filtered_clothes_set = ClothesSet.objects.filter(pk__in=filtered_clothes_set_id)

        analysis_upper_category_dict = {
            '하의' : [],
            '원피스' : [],
            '아우터' : [],
            '치마' : [],
            '상의' : []        
        }

        for clothes_set in filtered_clothes_set:
            for clothes in clothes_set.clothes.all():
                analysis_upper_category_dict[clothes.upper_category].append(clothes.lower_category)

        for key in analysis_upper_category_dict.keys():
            if len(analysis_upper_category_dict[key]) == 0:
                analysis_upper_category_dict[key] = ""
                continue

            analysis_upper_category_dict[key] = mode(analysis_upper_category_dict[key])

        return Response(analysis_upper_category_dict)    


class ClothesNestedView(FiltersMixin, NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Clothes.objects.all()
    serializer_class = ClothesSerializer  
    
    # Apply ordering, uses `ordering` query parameter.
    filter_backends = (filters.OrderingFilter, )
    ordering_fields = ('created_at', 'id', )
    ordering = ('-created_at', )

    # Apply filtering, using other query parameters.
    filter_mappings = {
        'upper_category': 'upper_category',
        'lower_category': 'lower_category',
    }

    # Use filter validation.
    filter_validation_schema = clothes_query_schema
    
    # Permissions.
    permission_classes = [IsAuthenticatedOrReadOnly]


class ClothesSetView(FiltersMixin, NestedViewSetMixin, viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = ClothesSet.objects.all()
        
        # me 파라미터가 true인 경우, 해당 유저의 코디만 반환
        if self.request.query_params.get('me'):
            user = self.request.user
            queryset = queryset.filter(owner=user.id)
                
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return ClothesSetSerializer
        return ClothesSetReadSerializer 

    # Apply ordering, uses `ordering` query parameter.
    filter_backends = (filters.OrderingFilter, )
    ordering_fields = ('created_at', 'id', )
    ordering = ('-created_at', )

    # Apply filtering, using other query parameters.
    filter_mappings = {
        'style': 'style',
    }

    # Use filter validation.
    filter_validation_schema = clothes_set_query_schema
    
    # Permissions.
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def list(self, request, *args, **kwargs):
        # If me parameter is set, check authentication.
        if request.query_params.get('me') and not request.user.is_authenticated:
            return Response({
                'error' : 'token authorization failed ... please log in'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        queryset = self.filter_queryset(self.get_queryset())
        if request.query_params.get('review'):
            reviews = ClothesSetReview.objects.all()
            
            queryset_list = list(queryset)
            for clothesSet in queryset_list:
                included_reviews = reviews.filter(clothes_set__id=clothesSet.id)
                if len(included_reviews) == 0:
                    queryset = queryset.exclude(id=clothesSet.id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
            
        return Response(serializer.data)
            
    
    def create(self, request, *args, **kwargs):
        if 'clothes' in request.data.keys():
            user = request.user
            
            all_clothes = Clothes.objects.all()
            filtered_clothes = all_clothes.filter(owner_id=user.id)
            filtered_clothes_id = []
            for clothes in filtered_clothes:
                filtered_clothes_id.append(int(clothes.id))
                
            # 입력된 옷들이 모두 해당 유저의 것인지 확인.
            # TODO(mskwon1): content-type이 json이 아닌경우 바꿔줘야함.
            # for clothes_id in request.data.getlist('clothes'):
            for clothes_id in request.data['clothes']:
                if int(clothes_id) not in filtered_clothes_id:
                    return Response({
                        "error" : "this is not your clothes : " + clothes_id
                    }, status=status.HTTP_200_OK)
        
        if 'image' in request.data.keys():
            image = byte_to_image(request.data['image'])
            temp_url = save_image_s3(image, 'clothes-sets')
            image_url = move_image_to_saved(temp_url, 'clothes-sets')
            
            request.data['image_url'] = image_url
        
        else:
            return Response({
                "error": 'image field is required'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(owner_id = self.request.user.id)

    def update(self, request, *args, **kwargs):
        user = request.user
        key = int(kwargs.pop('pk'))
        target_clothes_set = ClothesSet.objects.filter(id=key)
        
        if user.id != int(target_clothes_set[0].owner.id):
            return Response({
                'error' : 'you are not allowed to access this object'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        if 'image' in request.data.keys():
            image = byte_to_image(request.data['image'])
            temp_url = save_image_s3(image, 'clothes-sets')
            image_url = move_image_to_saved(temp_url, 'clothes-sets')
            
            request.data['image_url'] = image_url
            
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        user = request.user
        key = int(kwargs.pop('pk'))
        target_clothes_set = ClothesSet.objects.filter(id=key)
        
        if user.id != int(target_clothes_set[0].owner.id):
            return Response({
                'error' : 'you are not allowed to access this object'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        return super().destroy(request, *args, **kwargs)
    
    
class ClothesSetNestedView(FiltersMixin, NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = ClothesSet.objects.all()
    serializer_class = ClothesSetReadSerializer  
    
    # Apply ordering, uses `ordering` query parameter.
    filter_backends = (filters.OrderingFilter, )
    ordering_fields = ('created_at', 'id', )
    ordering = ('-created_at', )

    # Apply filtering, using other query parameters.
    filter_mappings = {
        'style': 'style',
    }

    # Use filter validation.
    filter_validation_schema = clothes_set_query_schema
    
    # Permissions.
    permission_classes = [IsAuthenticatedOrReadOnly]
        
        
class ClothesSetReviewView(FiltersMixin, NestedViewSetMixin, viewsets.ModelViewSet):    
    def get_queryset(self):
        queryset = ClothesSetReview.objects.all()
        
        # me 파라미터가 true인 경우, 해당 유저의 Review만 반환
        if self.request.query_params.get('me'):
            user = self.request.user
            queryset = queryset.filter(owner=user.id)
                
        return queryset

    def  get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return ClothesSetReviewSerializer
        return ClothesSetReviewReadSerializer

    # Apply ordering, uses `ordering` query parameter.
    filter_backends = (filters.OrderingFilter, )
    ordering_fields = ('created_at', 'id', )
    ordering = ('-created_at', )

    # Apply filtering, using other query parameters.
    filter_mappings = {
        'start_datetime': 'start_datetime__gte',
        'end_datetime': 'end_datetime__lte',
        'location' : 'location',
        'review': 'review',
    }

    # Use filter validation.
    filter_validation_schema = clothes_set_review_query_schema
    
    # Permissions.
    permission_classes = [IsAuthenticatedOrReadOnly]    
    
    def list(self, request, *args, **kwargs):
        # If me parameter is set, check authentication.
        if request.query_params.get('me') and not request.user.is_authenticated:
            return Response({
                'error' : 'token authorization failed ... please log in'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        queryset = self.filter_queryset(self.get_queryset())

        max_temp = request.query_params.get('max_sensible_temp')
        min_temp = request.query_params.get('min_sensible_temp')
        
        if max_temp is not None:
            max_temp = float(max_temp)
            queryset = queryset.filter(max_sensible_temp__lte=(max_temp+2), max_sensible_temp__gte=(max_temp-2))

        if min_temp is not None:
            min_temp = float(min_temp)
            queryset = queryset.filter(min_sensible_temp__lte=(min_temp+2), min_sensible_temp__gte=(min_temp-2))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        if 'clothes_set' in request.data:
            user = request.user
            
            all_clothes_set = ClothesSet.objects.all()
            filtered_clothes_set = all_clothes_set.filter(owner_id=user.id)
            filtered_clothes_set_id = []
            for clothes_set in filtered_clothes_set:
                filtered_clothes_set_id.append(int(clothes_set.id))
                
            # 입력된 코디가 해당 유저의 것인지 확인.
            if int(request.data['clothes_set']) not in filtered_clothes_set_id:
                return Response({
                    "error" : "this is not your clothes set : " + request.data['clothes_set']
                }, status=status.HTTP_200_OK)
        
        if set(['clothes_set', 'start_datetime', 'end_datetime', 'location', 'review']).issubset(request.data.keys()):
            start = request.data['start_datetime']
            end = request.data['end_datetime']
            location = int(request.data['location'])
            start_date = start.split('T')[0]
            start_time = int(start.split('T')[1].split(':')[0])
            end_date = end.split('T')[0]
            end_time = int(end.split('T')[1].split(':')[0])
            
            # API 요청하기
            all_weather_data = Weather.objects.all()
            weather_data_set = all_weather_data.filter(location_code=location)
            weather_data_on_start = weather_data_set.filter(date__gte=start_date, time__gte=start_time)
            weather_data_on_end = weather_data_on_start.filter(date__lte=end_date, time__lte=end_time)

            if weather_data_on_end.count()==0:
                now = datetime.datetime.now()
                today = now - datetime.timedelta(hours=24)

                if start < today:
                    return Response({
                        'error' : 'please try again later'
                    }, status=status.HTTP_404_NOT_FOUND)

                else:
                    with open('apps/api/locations/data.json') as json_file:
                        json_data = json.load(json_file)
                    
                    new_x = int((json_data[str(location)]['x']))
                    new_y = int((json_data[str(location)]['y']))    

                    date_list = [start, end]

                    for date_time in date_list:
                        date = date_time.strftime('%Y-%m-%d %H:%M:%S')
                        year_month_day = date[0].split('-')
                        year = year_month_day[0]
                        month = year_month_day[1]
                        day = year_month_day[2]
                        conv_time = date[1].split(':')
                        conv_time = conv_time[0] + conv_time[1]
                        conv_time, conv_date = convert_time(conv_time, year, month, day)
            
                        response = get_weather_date(date, str(location))
                        weather_data_on_end.objects.create(location_code=location, date=date[0:10], time=conv_time[0:2], x=new_x, y=new_y,
                                                            temp=response['T3H'], sensible_temp=response['WCI'], humidity=response['REH'], 
                                                            wind_speed=response['WSD'], precipitation=response['R06'])
                                                                  
            request.data['max_temp'] = weather_data_on_end.aggregate(Max('temp'))['temp__max']
            request.data['min_temp'] = weather_data_on_end.aggregate(Min('temp'))['temp__min']
            request.data['max_sensible_temp'] = weather_data_on_end.aggregate(Max('sensible_temp'))['sensible_temp__max']
            request.data['min_sensible_temp'] = weather_data_on_end.aggregate(Min('sensible_temp'))['sensible_temp__min']
            request.data['humidity'] = weather_data_on_end.aggregate(Avg('humidity'))['humidity__avg']
            request.data['wind_speed'] = weather_data_on_end.aggregate(Avg('wind_speed'))['wind_speed__avg']
            request.data['precipitation'] = weather_data_on_end.aggregate(Avg('precipitation'))['precipitation__avg']
        
        return super(ClothesSetReviewView, self).create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(
            owner_id=self.request.user.id
        )

    def update(self, request, *args, **kwargs):
        user = request.user
        key = int(kwargs.pop('pk'))
        target_clothes_review_set = ClothesSetReview.objects.filter(id=key)
        
        if user.id != int(target_clothes_review_set[0].owner.id):
            return Response({
                'error' : 'you are not allowed to access this object'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if set(['clothes_set', 'start_datetime', 'end_datetime', 'location', 'review']).issubset(request.data.keys()):
            start = request.data['start_datetime']
            end = request.data['end_datetime']
            location = int(request.data['location'])
            start_date = start.split('T')[0]
            start_time = int(start.split('T')[1].split(':')[0])
            end_date = end.split('T')[0]
            end_time = int(end.split('T')[1].split(':')[0])
            
            # API 요청하기
            all_weather_data = Weather.objects.all()
            weather_data_set = all_weather_data.filter(location_code=location)
            weather_data_on_start = weather_data_set.filter(date__gte=start_date, time__gte=start_time)
            weather_data_on_end = weather_data_on_start.filter(date__lte=end_date, time__lte=end_time)

            if weather_data_on_end.count()==0:
                with open('apps/api/locations/data.json') as json_file:
                    json_data = json.load(json_file)
                
                new_x = int((json_data[str(location)]['x']))
                new_y = int((json_data[str(location)]['y']))    

                date_list = [start, end]

                for date_time in date_list:
                    date = date_time.strftime('%Y-%m-%d %H:%M:%S')
                    year_month_day = date[0].split('-')
                    year = year_month_day[0]
                    month = year_month_day[1]
                    day = year_month_day[2]
                    conv_time = date[1].split(':')
                    conv_time = conv_time[0] + conv_time[1]
                    conv_time, conv_date = convert_time(conv_time, year, month, day)
        
                    response = get_weather_date(date, str(location))
                    weather_data_on_end.objects.create(location_code=location, date=date[0:10], time=conv_time[0:2], x=new_x, y=new_y,
                                                        temp=response['T3H'], sensible_temp=response['WCI'], humidity=response['REH'], 
                                                        wind_speed=response['WSD'], precipitation=response['R06'])

                                                        
            
            request.data['max_temp'] = weather_data_on_end.aggregate(Max('temp'))['temp__max']
            request.data['min_temp'] = weather_data_on_end.aggregate(Min('temp'))['temp__min']
            request.data['max_sensible_temp'] = weather_data_on_end.aggregate(Max('sensible_temp'))['sensible_temp__max']
            request.data['min_sensible_temp'] = weather_data_on_end.aggregate(Min('sensible_temp'))['sensible_temp__min']
            request.data['humidity'] = weather_data_on_end.aggregate(Avg('humidity'))['humidity__avg']
            request.data['wind_speed'] = weather_data_on_end.aggregate(Avg('wind_speed'))['wind_speed__avg']
            request.data['precipitation'] = weather_data_on_end.aggregate(Avg('precipitation'))['precipitation__avg']
        
        return super(ClothesSetReviewView, self).update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        user = request.user
        key = int(kwargs.pop('pk'))
        target_clothes_review_set = ClothesSetReview.objects.filter(id=key)
        
        if user.id != int(target_clothes_review_set[0].owner.id):
            return Response({
                'error' : 'you are not allowed to access this object'
            }, status=status.HTTP_401_UNAUTHORIZED)

        return super().destroy(request, *args, **kwargs)    
    
    @action(detail=False, methods=['get'])
    def location_search(self, request, *args, **kwargs):
        """
        An endpoint that returns search result for
        location based on query parameter
        """
        
        # Get query parameters.
        search = request.query_params.get('search')
        search = '' if search == None else search
        limit = request.query_params.get('limit')
        offset = request.query_params.get('offset')
        
        # Open JSON file for location results.
        with open('apps/api/locations/data.json') as json_file:
            data = json.load(json_file)
            
        # Get results total count & initial list containing search keyword.    
        results = []
        count = 0
        for index in data:
            if search in data[index]['full_address']:
                count += 1
                results.append({
                    'id' : index,
                    'location' : data[index]['full_address']
                })
        
        # Filter list according to limit & offset.
        final_results = []
        offset = 0 if offset == None else int(offset)
        limit = count if limit == None else int(limit)
        limit_count = 0
        
        for result in results[offset:]:
            limit_count += 1
            final_results.append(result)
            if limit_count == limit:
                break
        
        # Return response.
        return Response({
                'count': count,
                'next': offset + limit_count,
                'results': final_results,
            }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def global_weather(self, request, *args, **kwargs):
        """
        An endpoint that returns global weather data for 
        location and date which wanna forecast
        """
        # Get Location.
        city_name = request.query_params.get('city_name')
        forecast_date = request.query_params.get('date')
        weather_data = get_global_weather_city_name(forecast_date, city_name)
        temperature = float(weather_data['TEMP'])
        max_temp = float(weather_data['MAX'])
        min_temp = float(weather_data['MIN'])
        humidity = int(weather_data['REH'])
        wind_speed = float(weather_data['WSD'])
        precipitation = float(weather_data['PRE'])
        sense = float(weather_data['WCI'])
        max_sense = float(weather_data['WCIMAX'])
        min_sense = float(weather_data['WCIMIN'])

        return Response({
        'temperature': temperature,
        'min_temperature': min_temp,
        'max_temperature': max_temp,
        'chill_temp': sense,
        'min_chill_temp': min_sense,
        'max_chill_temp': max_sense,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'precipitation': precipitation,
            }, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['get'])
    def global_search(self, request, *args, **kwargs):
        """
        An endpoint that returns search result for
        location based on query parameter
        """
        
        # Get query parameters.
        search = request.query_params.get('search')
        search = '' if search == None else search
        limit = request.query_params.get('limit')
        offset = request.query_params.get('offset')
        
        # Open JSON file for location results.
        with open('apps/api/locations/cities_20000.json', 'rt', encoding='UTF-8') as json_file:
            data = json.load(json_file)
            
        # Get results total count & initial list containing search keyword.    
        results = []
        count = 0
        for city in data:
            if search in city['city_name']:
                count += 1
                results.append({
                    'id': city['city_id'],
                    'location' : city['city_name']
                })
        
        # Filter list according to limit & offset.
        final_results = []
        offset = 0 if offset == None else int(offset)
        limit = count if limit == None else int(limit)
        limit_count = 0
        
        for result in results[offset:]:
            limit_count += 1
            final_results.append(result)
            if limit_count == limit:
                break
        
        # Return response.
        return Response({
                'count': count,
                'next': offset + limit_count,
                'results': final_results,
            }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def current_weather(self, request, *args, **kwargs):
        """
        An endpoint that returns weather data for
        location based on query parameter and current time
        """
        # Get Location.
        location = request.query_params.get('location')
        weather_data = get_current_weather(location)
        temperature = float(weather_data['T1H'])
        max_temp = float(weather_data['MAX'])
        min_temp = float(weather_data['MIN'])
        humidity = int(weather_data['REH'])
        wind_speed = float(weather_data['WSD'])
        precipitation = float(weather_data['RN1'])
        sense = float(weather_data['WCI'])
        max_sense = float(weather_data['WCIMAX'])
        min_sense = float(weather_data['WCIMIN'])

        # Return response
        return Response({
                'temperature': temperature,
                'min_temperature': min_temp,
                'max_temperature': max_temp,
                'chill_temp': sense,
                'min_chill_temp': min_sense,
                'max_chill_temp': max_sense,
                'humidity': humidity,
                'wind_speed': wind_speed,
                'precipitation': precipitation,
            }, status=status.HTTP_200_OK)

class ClothesSetReviewNestedView(FiltersMixin, NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = ClothesSetReview.objects.all()
    serializer_class = ClothesSetReviewReadSerializer  

    # Apply ordering, uses `ordering` query parameter.
    filter_backends = (filters.OrderingFilter, )
    ordering_fields = ('created_at', 'id', )
    ordering = ('-created_at', )

    # Apply filtering, using other query parameters.
    filter_mappings = {
        'start_datetime': 'start_datetime',
        'end_datetime': 'end_datetime',
        'location' : 'location',
        'max_sensible_temp' : 'max_sensible_temp',
        'min_sensible_temp ' : 'min_sensible_temp',
    }

    # Use filter validation.
    filter_validation_schema = clothes_set_review_query_schema
    
    # Permissions.
    permission_classes = [IsAuthenticatedOrReadOnly]   
