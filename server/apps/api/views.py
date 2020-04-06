import datetime
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
from .models import Clothes, ClothesSet, ClothesSetReview, User
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
from .weather import get_weather_date, get_weather_between, get_weather_time_date

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
        'upper_category': 'upper_category',
        'lower_category': 'lower_category',
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
                request.data['image_url']  = move_image_to_saved(image_url)
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
        image = byte_to_image(request.body)
        image = remove_background(image)
        image_url = save_image_s3(image)
        
        image_tensor = image_to_tensor(image)
        inference_result = execute_inference(image_tensor)
        upper, lower = get_categories_from_predictions(inference_result)
        
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


class ClothesSetView(FiltersMixin, NestedViewSetMixin, viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = ClothesSet.objects.all()
        
        # me 파라미터가 true인 경우, 해당 유저의 코디만 반환
        if self.request.query_params.get('me'):
            user = self.request.user
            queryset = queryset.filter(owner=user.id)
                
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create' or 'update':
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
            
        return super().list(request, *args, **kwargs)
    
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
        
class ClothesSetReviewView(FiltersMixin, NestedViewSetMixin, viewsets.ModelViewSet):    
    def get_queryset(self):
        queryset = ClothesSetReview.objects.all()
        
        # me 파라미터가 true인 경우, 해당 유저의 Review만 반환
        if self.request.query_params.get('me'):
            user = self.request.user
            queryset = queryset.filter(owner=user.id)
                
        return queryset

    def  get_serializer_class(self):
        if self.action == 'create' or 'update':
            return ClothesSetReviewSerializer
        return ClothesSetReviewReadSerializer

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
    
    def list(self, request, *args, **kwargs):
        # If me parameter is set, check authentication.
        if request.query_params.get('me') and not request.user.is_authenticated:
            return Response({
                'error' : 'token authorization failed ... please log in'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        return super().list(request, *args, **kwargs)
    
    # TODO(mskwon1): 날씨정보 받아오기
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
        
        if set(['clothes_set', 'start_datetime', 'end_datetime', 'location', 'review' ]).issubset(request.data.keys()):
            start = request.data['start_datetime']
            end = request.data['end_datetime']
            location = request.data['location']
            
            # API 요청하기
            start_weather = get_weather_date(start, location)
            end_weather = get_weather_date(end, location)

            # 온도 구하기
            start_min = start_weather['TMN']
            start_max = start_weather['TMX']

            # API 요청하기
            weather_data = get_weather_between(start, end, location)
            
            # 온도 구하기

            maximum_temp = weather_data['MAX']
            minimum_temp = weather_data['MIN']
            maximum_sensible_temp = weather_data['WCIMAX']
            minimum_sensible_temp = weather_data['WCIMIN']

            # 데이터 저장하기
            min_temp = minimum_temp

            humidity =  weather_data['REH']
            precipitation =  weather_data['R06']
            wind_speed = weather_data['WSD']

            # self.get_serializer(data=request.data) request.data에 정보 넣기
            request.data['max_temp'] = maximum_temp 
            request.data['min_temp'] = minimum_temp
            request.data['max_sensible_temp'] = maximum_sensible_temp
            request.data['min_sensible_temp'] = minimum_sensible_temp
            request.data['humidity'] = humidity
            request.data['wind_speed'] = wind_speed
            request.data['percipitation'] = precipitation
            
            start_cur = start_weather['T3H']
            start_sense_max = start_weather['WCIMAX']
            start_sense_min = start_weather['WCIMIN']
            start_sense = start_weather['WCI']

            end_min = end_weather['TMN']
            end_max = end_weather['TMX']

            end_sense_max = end_weather['WCIMAX']
            end_sense_min = end_weather['WCIMIN']
            end_cur = end_weather['T3H']
            end_sense = end_weather['WCI']

            maximum_temp = max(start_cur, end_cur)
            minimum_temp = min(start_cur, end_cur)
            
            maximum_sensible_temp =  max(start_sense, end_sense)
            minimum_sensible_temp =  min(start_sense, end_sense)

            # 데이터 저장하기
            min_temp = minimum_temp
            max_sensible_temp = maximum_sensible_temp
            min_sensible_temp = minimum_sensible_temp
            humidity =  start_weather['REH']
            precipitation =  start_weather['R06']
            wind_speed = start_weather['WSD']

            # self.get_serializer(data=request.data) request.data에 정보 넣기
            request.data['max_temp'] = float(maximum_temp)
            request.data['min_temp'] = float(minimum_temp)
            request.data['max_sensible_temp'] = float(maximum_sensible_temp)
            request.data['min_sensible_temp'] = float(minimum_sensible_temp)
            request.data['humidity'] = int(humidity)
            request.data['wind_speed'] = float(wind_speed)
            request.data['precipitation'] = int(precipitation)
        
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
        
        
        if set(['clothes_set', 'start_datetime', 'end_datetime', 'location', 'review' ]).issubset(request.data.keys()):
            start = request.data['start_datetime']
            end = request.data['end_datetime']
            location = request.data['location']
            # API 요청하기
            start_weather = get_weather_date(start, location)
            end_weather = get_weather_date(end, location)

            # 온도 구하기
            start_min = start_weather['TMN']
            start_max = start_weather['TMX']
            
            start_cur = start_weather['T3H']
            start_sense_max = start_weather['WCIMAX']
            start_sense_min = start_weather['WCIMIN']
            start_sense = start_weather['WCI']

            end_min = end_weather['TMN']
            end_max = end_weather['TMX']

            end_sense_max = end_weather['WCIMAX']
            end_sense_min = end_weather['WCIMIN']
            end_cur = end_weather['T3H']
            end_sense = end_weather['WCI']

            maximum_temp = max(start_cur, end_cur)
            minimum_temp = min(start_cur, end_cur)
            
            maximum_sensible_temp =  max(start_sense, end_sense)
            minimum_sensible_temp =  min(start_sense, end_sense)

            # 데이터 저장하기
            min_temp = minimum_temp
            max_sensible_temp = maximum_sensible_temp
            min_sensible_temp = minimum_sensible_temp
            humidity =  start_weather['REH']
            precipitation =  start_weather['R06']
            wind_speed = start_weather['WSD']

            # self.get_serializer(data=request.data) request.data에 정보 넣기
            request.data['max_temp'] = float(maximum_temp)
            request.data['min_temp'] = float(minimum_temp)
            request.data['max_sensible_temp'] = float(maximum_sensible_temp)
            request.data['min_sensible_temp'] = float(minimum_sensible_temp)
            request.data['humidity'] = int(humidity)
            request.data['wind_speed'] = float(wind_speed)
            request.data['precipitation'] = int(precipitation)
        
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
