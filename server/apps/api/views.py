from bs4 import BeautifulSoup
import datetime
from dateutil.parser import parse
from django.db.models import Avg, Max, Min, Sum
from django.utils import timezone
from filters.mixins import FiltersMixin
import json
from random import sample
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import requests
from statistics import mode

from .exceptions import S3FileError
from .globalweather import get_global_weather_city_name
from .models import Clothes, ClothesSet, ClothesSetReview, ReviewSensor, User, Weather
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
        
        MAX_ITEM_NUM = 3
        MAX_IMAGE_NUM = 3

        min_temp = float(request.query_params.get('minTemp'))
        max_temp = float(request.query_params.get('maxTemp'))
        wind_speed = float(request.query_params.get('windSpeed'))
        humidity = float(request.query_params.get('humidity'))
        
        weather_type = get_weather_class([max_temp, min_temp, wind_speed, humidity])
        cody_review_set = ClothesSetReview.objects.all()
        filtered_cody_review_set = cody_review_set.filter(review=3, weather_type=weather_type)

        filtered_clothes_set_id = []
        for filtered_cody_review in filtered_cody_review_set:
            filtered_clothes_set_id.append(filtered_cody_review.clothes_set.id)
        
        filtered_clothes_set = ClothesSet.objects.filter(pk__in=filtered_clothes_set_id)
        
        combination_dict = {}
        for clothes_set in filtered_clothes_set:
            clothes_combination = set()
            for clothes in clothes_set.clothes.all():
                clothes_combination.add(clothes.lower_category)
                
            comb = tuple(clothes_combination)
            if comb in combination_dict.keys():
                combination_dict[comb][0] += 1
                combination_dict[comb][1].add(clothes_set.image_url)
            else:
                combination_dict[comb] = [1,set([clothes_set.image_url])]
        
        result = sorted(combination_dict.items(), key=(lambda x:x[1][0]), reverse=True)[:MAX_ITEM_NUM]

        result_list = []
        for item in result:
            item = list(item)
            result_dict = {}
            result_dict['combination'] = '-'.join(list(item[0]))
            images_list = list(item[1][1])

            if len(images_list) > MAX_IMAGE_NUM:
                images_list = sample(images_list, MAX_IMAGE_NUM)

            result_dict['images'] = images_list
            result_list.append(result_dict)

        return Response(result_list)

    
    @action(detail=False, methods=['get'])
    def lookbook(self, request, *args, **kwargs):
        """
        An endpoint where the lookbook is returned
        """
        now = datetime.datetime.now()
        year = str(now.year)
        user_gender = request.user.gender
        if user_gender=='남자':
            user_gender = 'm'
        else:
            user_gender = 'f'

        url = 'https://www.musinsa.com/index.php?m=shopstaff&_y=' + year + '&ordw=d_regis&gender=' + user_gender
        
        req = requests.get(url)
        html = BeautifulSoup(req.text, 'html.parser')
        div_tag = html.find('div', class_='list-box box')

        # 0~9 랜덤 숫자 5개 뽑기
        num_list = sample([0,1,2,3,4,5,6,7,8,9], 5)

        li_tag = div_tag.find_all('li', class_='listItem')
        
        lookbook_list = []
        for count in range(5):
            ran_img = int(num_list[count])
            ran_li = li_tag[ran_img]

            # 이미지 url 받아오기
            img_url = ran_li.find('img').get('src')
            img_url = img_url.replace('//','http://')

            # 브랜드명 받아오기
            brand = ran_li.find('p', class_='brackets brand').text

            # 모델 이름 받아오기
            name = ran_li.find('span').text

            lookbook = {'image' : img_url, 'brand' : brand, 'name' : name}
            lookbook_list.append(lookbook)

        return Response(lookbook_list)


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

        max_temp = float(request.query_params.get('maxTemp'))
        min_temp = float(request.query_params.get('minTemp'))
        wind_speed = float(request.query_params.get('windSpeed'))
        humidity = float(request.query_params.get('humidity'))
        
        weather_type = get_weather_class([max_temp, min_temp, wind_speed, humidity])
        queryset = queryset.filter(weather_type=weather_type)

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

        # 하루 시간대 (0-8, 8-16, 16-24)
        day = [0, 8, 16, 24] 
        
        if set(['clothes_set', 'start_datetime', 'end_datetime', 'location']).issubset(request.data.keys()):
            start = request.data['start_datetime']
            end = request.data['end_datetime']
            location = int(request.data['location'])
            fix_start_date = start.split('T')[0]
            fix_start_time = start.split('T')[1].split(':')
            fix_end_date = end.split('T')[0]
            fix_end_time = end.split('T')[1].split(':')

            start_year_month_day = fix_start_date.split('-')
            fix_start_year = start_year_month_day[0] # 년
            fix_start_month = start_year_month_day[1] # 월
            fix_start_day = start_year_month_day[2] # 일

            end_year_month_day = fix_end_date.split('-')
            fix_end_year = end_year_month_day[0]
            fix_end_month = end_year_month_day[1]
            fix_end_day = end_year_month_day[2]

            # 리뷰가 여러 날짜에 걸치는 경우를 위해 날짜 차이 계산
            d1 = start.split('T')[0].split('-')
            d2 = end.split('T')[0].split('-')
            t1 = datetime.datetime(int(d1[0]), int(d1[1]), int(d1[2]), 0, 0, 0)
            t2 = datetime.datetime(int(d2[0]), int(d2[1]), int(d2[2]), 0, 0, 0)
            
            diff_date = (t2 - t1).days

            start_time =  [fix_start_time[0], fix_start_time[1], fix_start_time[2]]
            end_time = [fix_end_time[0], fix_end_time[1], fix_end_time[2]]
            start_year = fix_start_year
            start_month = fix_start_month
            start_day = fix_start_day
            end_year = fix_end_year
            end_month = fix_end_month
            end_day = fix_end_day

            # 날짜 만큼 반복
            for d in range(0, diff_date+1):
                if(diff_date != 0): # start_date != end_date
                    if(d == 0): # start_date != end_date & 첫 날
                        end_time[0] = "23"
                        end_time[1] = "59"
                        end_time[2] = "59"
                        end_year = fix_start_year
                        end_month = fix_start_month
                        end_day = fix_start_day
                    elif(d == diff_date): # start_date != end_date & 마지막 날
                        start_time[0] = "00"
                        start_time[1] = "00"
                        start_time[2] = "00"
                        start_year = fix_end_year
                        start_month = fix_end_month
                        start_day = fix_end_day
                        end_time = fix_end_time
                        end_year = fix_end_year
                        end_month = fix_end_month
                        end_day = fix_end_day
                    else: # start_date != end_date & 중간 날
                        start_time = fix_start_time
                        start_time[0] = "00"
                        start_time[1] = "00"
                        start_time[2] = "00"
                        if((start_month == "12") & (start_day + 1 > 31)): # 년 단위 변화
                            start_year = int(start_year) + 1
                            start_month = "01"
                            start_day = "01"
                        elif(start_day + 1 > 28): # 달 단위 변화
                            if(fix_start_month == 2):
                                start_month = int(start_month) + 1
                                start_day = "01"
                            elif(start_month % 2 == 0): # 짝수 달
                                if(start_day + 1 > 30):
                                    start_month = int(start_month) + 1
                                    start_day = int(start_day) + 1
                                else:
                                    start_day = int(start_day) + 1
                            else: # 홀수 달
                                if(start_day + 1 > 31):
                                    start_month = int(start_month) + 1
                                    start_day = int(start_day) + 1
                                else:
                                    start_day = int(start_day) + 1
                        else: # 일 단위 변화
                            start_day = int(start_day) + 1

                        end_year = start_year
                        end_month = start_month
                        end_day = start_day

                # 시작 시간대 구분
                if(int(start_time[0]) < 8): # 시작시간 : 아침
                    st = 1
                elif(int(start_time[0]) < 16): # 시작시간 : 오후
                    st = 2
                else: # 시작시간 : 밤
                    st = 3

                # 끝 시간대 구분
                if(int(end_time[0]) < 8): # 끝시간 : 아침
                    et = 0
                elif(int(end_time[0]) < 16): # 끝시간 : 오후
                    et = 1
                else: # 끝시간 : 밤
                    et = 2              

                # 시작 ~ 끝 시간대 계산
                i = 0
                r = 0
                if(st-et == 1): # 끝-시작 = 시간대 1개
                    r = 1
                elif(st-et == 0): # 끝-시작 = 시간대 2개
                    r = 2
                else: # 끝-시작 = 시간대 3개
                    r = 3

                for i in range(0, r):
                    if(r==1): # 끝-시작 = 시간대 1개
                        start_conv_time = start_time[0] + start_time[1] # 시+분 ex_12:30 -> 1230
                        end_conv_time = end_time[0] + end_time[1]

                        real_start_time = start_time
                        real_start_time = str(real_start_time[0]) + ":" + str(real_start_time[1]) + ":" + str(real_start_time[2])
                        real_end_time = end_time
                        real_end_time = str(real_end_time[0]) + ":" + str(real_end_time[1]) + ":" + str(real_end_time[2])

                    elif(r==2): # 끝-시작 = 시간대 2개
                        if(i==0): # 앞 시간대
                            start_conv_time = start_time[0] + start_time[1] 
                            end_conv_time = day[st]*100
                            
                            real_start_time = start_time
                            real_start_time = str(real_start_time[0]) + ":" + str(real_start_time[1]) + ":" + str(real_start_time[2])
                            real_end_time = end_time
                            if(day[st] < 10):
                                real_end_time = "0" + str(day[st]) + ":" + '00' + ":" + '00'
                            else:
                                real_end_time = str(day[st]) + ":" + '00' + ":" + '00'
                            
                            
                            
                        else: # 뒷 시간대
                            start_conv_time = day[et]*100
                            end_conv_time = end_time[0] + end_time[1]

                            real_start_time = start_time
                            if(day[et] < 10):
                                real_start_time = "0" + str(day[et]) + ":" + '00' + ":" + '00'
                            else:
                                real_start_time = str(day[et]) + ":" + '00' + ":" + '00'
                            real_end_time = end_time
                            real_end_time = str(real_end_time[0]) + ":" + str(real_end_time[1]) + ":" + str(real_end_time[2])
                                                    

                    else: # 끝-시작 = 시간대 3개
                        if(i==0): # 앞 시간대
                            start_conv_time = start_time[0] + start_time[1] 
                            end_conv_time = day[st]*100
                            
                            real_start_time = start_time
                            real_start_time = str(real_start_time[0]) + ":" + str(real_start_time[1]) + ":" + str(real_start_time[2])
                            real_end_time = end_time
                            if(day[st] < 10):
                                real_end_time = "0" + str(day[st]) + ":" + '00' + ":" + '00'
                            else:
                                real_end_time = str(day[st]) + ":" + '00' + ":" + '00'
                            
                            
                        elif(i==1): # 중간 시간대
                            start_conv_time = day[st]*100
                            end_conv_time = day[et]*100

                            real_start_time = start_time
                            real_start_time = "0" + str(day[st]) + ":" + '00' + ":" + '00'
                            real_end_time = end_time
                            real_end_time = str(day[et]) + ":" + '00' + ":" + '00'

                        else: # 끝 시간대
                            start_conv_time = day[et]*100
                            end_conv_time = end_time[0] + end_time[1]

                            real_start_time = start_time
                            real_start_time = str(day[et]) + ":" + '00' + ":" + '00'
                            real_end_time = end_time
                            real_end_time = str(end_time[0]) + ":" + str(real_end_time[1]) + ":" + str(real_end_time[2])
                            

            
                    start_conv_time, start_conv_date = convert_time(start_conv_time, start_year, start_month, start_day)
                    start_conv_time = int(start_conv_time[0] + start_conv_time[1])
                    start_conv_date = start_conv_date[:4] + '-' + start_conv_date[4:6] + '-' + start_conv_date[6:]

                    end_conv_time, end_conv_date = convert_time(end_conv_time, end_year, end_month, end_day)
                    end_conv_time = int(end_conv_time[0] + end_conv_time[1])
                    end_conv_date = end_conv_date[:4] + '-' + end_conv_date[4:6] + '-' + end_conv_date[6:]
                    
                    # API 요청하기
                    all_weather_data = Weather.objects.all()
                    weather_data_set = all_weather_data.filter(location_code=location)
                    weather_data_set = weather_data_set.exclude(date__lt=start_conv_date)
                    weather_data_set = weather_data_set.exclude(date__gt=end_conv_date)
                    weather_data_on_start = weather_data_set.exclude(date=start_conv_date, time__lt=start_conv_time)
                    weather_data_on_end = weather_data_on_start.exclude(date=end_conv_date, time__gt=end_conv_time)
                    
                    if weather_data_on_end.count()==0:
                        now = datetime.datetime.now()
                        today = now - datetime.timedelta(hours=24)

                        if parse(start) < today:
                            return Response({
                                'error' : 'internal server error'
                            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

                                try:
                                    response = get_weather_date(date, str(location))
                                except:
                                    return Response({
                                        'error' : 'internal server error'
                                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                    
                    request.data['weather_type'] = get_weather_class([
                        request.data['max_temp'],
                        request.data['min_temp'],
                        request.data['wind_speed'],
                        request.data['humidity'],
                    ])

                    request.data['start_datetime'] = start_conv_date + " " + real_start_time
                    request.data['end_datetime'] = end_conv_date + " " + real_end_time

                    all_review_sensor = ReviewSensor.objects.all()
                    review_sensor_set = all_review_sensor.filter(owner_id=request.data['owner_id']) # owner_id=request.user.id
                    review_sensor_set = review_sensor_set.exclude(date__lt=start_conv_date)
                    review_sensor_set = review_sensor_set.exclude(date__gt=end_conv_date)
                    review_sensor_set = review_sensor_set.exclude(date=start_conv_date, time__lt=real_start_time)
                    review_sensor_set = review_sensor_set.exclude(date=end_conv_date, time__gt=real_end_time)

                    calc_review = review_sensor_set.aggregate(Sum('level'))['level__sum']
                    if(calc_review <= -4):
                        request.data['review'] = 1
                    elif(calc_review <= -2):
                        request.data['review'] = 2
                    elif(calc_review <= 1):
                        request.data['review'] = 3
                    elif(calc_review <= 3):
                        request.data['review'] = 4
                    else:
                        request.data['review'] = 5   

                    super(ClothesSetReviewView, self).update(request, *args, **kwargs)
    
        
        return Response({
                'owner_id': request.data['owner_id'],
            }, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(
            owner_id=self.request.user.id
        )

    def update(self, request, *args, **kwargs):
        user = request.user
        key = int(kwargs.pop('pk'))
        target_clothes_review_set = ClothesSetReview.objects.filter(owner_id=key)
        
        if user.id != int(target_clothes_review_set[0].owner.id):
            return Response({
                'error' : 'you are not allowed to access this object'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if set(['clothes_set', 'start_datetime', 'end_datetime', 'location']).issubset(request.data.keys()):
            start = request.data['start_datetime']
            end = request.data['end_datetime']
            location = int(request.data['location'])
            fix_start_date = start.split('T')[0]
            fix_start_time = start.split('T')[1].split(':')
            fix_end_date = end.split('T')[0]
            fix_end_time = end.split('T')[1].split(':')

            start_year_month_day = fix_start_date.split('-')
            fix_start_year = start_year_month_day[0] # 년
            fix_start_month = start_year_month_day[1] # 월
            fix_start_day = start_year_month_day[2] # 일

            end_year_month_day = fix_end_date.split('-')
            fix_end_year = end_year_month_day[0]
            fix_end_month = end_year_month_day[1]
            fix_end_day = end_year_month_day[2]

            cody_set = ClothesSetReview.objects.filter(owner_id=request.data['owner_id'], clothes_set_id=request.data['clothes_set'],
                                                        start_datetime__gte=start, end_datetime__lte=end)
            cody_set.update(comment=request.data['comment'])
            
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

    @action(detail=False, methods=['get'])
    def review_sensor(self, request, *args, **kwargs):
        """
        An endpoint where the review_sensor is returned
        """

        # owner = request.user.id
        owner = User.objects.filter(username=request.data['username'])
        owner = owner[0].id
        date = request.data['date']
        time = request.data['time']
        level = request.data['level']

        # TODO(hyobin) : gps 사용 여부 확인
        # x = request.data['x']
        # y = request.data['y']

        # with open('apps/api/locations/data.json') as json_file:
        #     json_data = json.load(json_file)

        # location_code = 0
        # for index in json_data:
        #     if json_data[index]['x'] == x:
        #         if json_data[index]['y'] == y:
        #             location = int(index)
        #             location_code = location
        #             break
        
        ReviewSensor.objects.create(owner_id=owner, date=date, time=time, level=level)

        return Response({
                        'owner_id' : owner,
                        'date' : date,
                        'time' : time, 
                        'level' : level,
                        })


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
