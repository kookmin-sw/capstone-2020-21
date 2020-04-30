from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.api.factories import (
    UserFactory,
    ClothesFactory,
    ClothesSetFactory,
    ClothesSetReviewFactory
)
from apps.api.populate import (
    populate_clothes,
    populate_clothes_set,
    populate_clothes_set_review
)

class ClohtesSetReviewCreateTests(APITestCase):
    def setUp(self):
        # Create a user and log in.
        created_user = UserFactory.create(
            username='test-username',
            password=make_password('test-password'),
            nickname='test-nickname',
            gender='남자',
            birthday='1996-01-14'
        )
        
        token_data = {
            'username': 'test-username',
            'password': 'test-password'
        }
        response = self.client.post('/api/token/', token_data, format='json')
        access_token = response.data['access']
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        
        # Create 10 Clothes for current user.
        populate_clothes(10)
        
        # Create 3 Clothes Set for current user.
        created_clothes_set = populate_clothes_set(3)

        self.clothes_set = created_clothes_set[0].id
        self.start_datetime = str(datetime.now() - timedelta(hours=12))
        self.start_datetime = 'T'.join(self.start_datetime.split(' '))
        self.end_datetime = str(datetime.now())
        self.end_datetime = 'T'.join(self.end_datetime.split(' '))
        self.location = 1
        self.review = 3
        self.comment = 'test-comment'
    
    def test_create(self):
        """
        정상생성 테스트.
        """
        data = {
            'clothes_set': self.clothes_set,
            'start_datetime': self.start_datetime,
            'end_datetime': self.end_datetime,
            'location': self.location,
            'review': self.review,
            'comment': self.comment
        }
        
        expected_keys = set([
            'id', 'clothes_set', 'start_datetime', 'end_datetime', 
            'location', 'review', 'max_temp', 'min_temp', 
            'max_sensible_temp', 'min_sensible_temp', 'humidity', 
            'wind_speed', 'precipitation', 'comment', 'owner'
        ])
        response = self.client.post('/clothes-set-reviews/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(set(response.data.keys()), expected_keys)
    
    def test_create_required(self):
        """
        필수필드생성 테스트.
        """
        data = {
            'clothes_set': self.clothes_set,
            'start_datetime': self.start_datetime,
            'end_datetime': self.end_datetime,
            'location': self.location,
            'review': self.review,
        }
        expected_keys = set([
            'id', 'clothes_set', 'start_datetime', 'end_datetime', 
            'location', 'review', 'max_temp', 'min_temp', 
            'max_sensible_temp', 'min_sensible_temp', 'humidity', 
            'wind_speed', 'precipitation', 'comment', 'owner'
        ])
        response = self.client.post('/clothes-set-reviews/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(set(response.data.keys()), expected_keys)
    
    def test_create_error_no_required(self):
        """
        오류 - 필수 필드 없을 경우.
        """
        data = {}
        response = self.client.post('/clothes-set-reviews/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['clothes_set'][0], 'This field is required.')
        self.assertEqual(response.data['start_datetime'][0], 'This field is required.')
        self.assertEqual(response.data['end_datetime'][0], 'This field is required.')
        self.assertEqual(response.data['location'][0], 'This field is required.')
        self.assertEqual(response.data['review'][0], 'This field is required.')
    
    def test_create_error_authentication(self):
        """
        오류 - 인증정보 오류.
        """
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.post('/clothes-set-reviews/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

class ClothesSetReviewRetrieveTests(APITestCase):
    def setUp(self):
        # Create a user and log in.
        created_user = UserFactory.create(
            username='test-username',
            password=make_password('test-password'),
            nickname='test-nickname',
            gender='남자',
            birthday='1996-01-14'
        )
        
        token_data = {
            'username': 'test-username',
            'password': 'test-password'
        }
        response = self.client.post('/api/token/', token_data, format='json')
        access_token = response.data['access']
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        
        # Create 10 Clothes for current user
        populate_clothes(10)
        
        # Create 3 ClothesSets for current user
        created_clothes_set = populate_clothes_set(3)
        
        # Create 3 ClothesSetReviews for current user
        self.created_review = populate_clothes_set_review(3)
    
        self.clothes_set = created_clothes_set[0].id
        self.start_datetime = str(datetime.now() - timedelta(hours=12))
        self.start_datetime = 'T'.join(self.start_datetime.split(' '))
        self.end_datetime = str(datetime.now())
        self.end_datetime = 'T'.join(self.end_datetime.split(' '))
        self.location = 1
        self.review = 3
        self.comment = 'test-comment'
        
    def test_retrieve_one(self):
        """
        단일 리뷰 정보 반환 테스트.
        """
        url = '/clothes-set-reviews/' + str(self.created_review[0].id) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_retrieve_many(self):
        """
        여러 개 리뷰 정보 반환 테스트.
        """
        response = self.client.get('/clothes-set-reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        
    def test_retrieve_me(self):
        """
        내 리뷰 정보 반환 테스트.
        """
        # Create new user.
        created_user = UserFactory.create(
            username='test-username-2',
            password=make_password('test-password'),
            nickname='test-nickname-2',
            gender='남자',
            birthday='1996-01-14'
        )
        
        # Create one clothes for new user.
        created_clothes = ClothesFactory.create(
            upper_category='상의',
            lower_category='반팔티셔츠',
            image_url='https://www.test_img.com',
            alias='test-alias',
            created_at=timezone.now(),
            owner_id=created_user.id
        )
        
        # Create one clothes set for new user.
        new_clothes_set = ClothesSetFactory.create(
            name='test-name', 
            style='화려',
            image_url='https://www.naver.com',
            created_at=timezone.now(),
            clothes=[created_clothes],
            owner=created_user
        )
        
        # Creates one clothes set review for new user.
        ClothesSetReviewFactory.create(
            start_datetime=self.start_datetime, 
            end_datetime=self.end_datetime, 
            location=self.location,
            review=self.review,
            max_temp=14.3,
            min_temp=2.4,
            max_sensible_temp=13.4, 
            min_sensible_temp=0.6, 
            humidity=40,
            wind_speed=5.2,
            precipitation=4,
            comment=self.comment,
            created_at=timezone.now(),
            clothes_set_id=new_clothes_set.id,
            owner=created_user
        )
        
        # Total Reviews : 4.
        response = self.client.get('/clothes-set-reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 4)
        
        # Current User's Review sets : 3.
        response = self.client.get('/clothes-set-reviews/?me=True')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
    
class ClothesSetReviewUpdateTests(APITestCase):
    def setUp(self):
        # Create a user and log in.
        created_user = UserFactory.create(
            username='test-username',
            password=make_password('test-password'),
            nickname='test-nickname',
            gender='남자',
            birthday='1996-01-14'
        )
        
        token_data = {
            'username': 'test-username',
            'password': 'test-password'
        }
        response = self.client.post('/api/token/', token_data, format='json')
        access_token = response.data['access']
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        
        # Create 10 Clothes for current user
        populate_clothes(10)
        
        # Create 3 ClothesSets for current user
        created_clothes_set = populate_clothes_set(3)
        
        # Create 1 ClothesSetReviews for current user
        self.created_review = populate_clothes_set_review(1)[0]
    
        self.clothes_set = created_clothes_set[0].id
        self.start_datetime = str(datetime.now() - timedelta(hours=12))
        self.start_datetime = 'T'.join(self.start_datetime.split(' '))
        self.end_datetime = str(datetime.now())
        self.end_datetime = 'T'.join(self.end_datetime.split(' '))
        self.location = 1
        self.review = 3
        self.comment = 'test-comment'
    
    def test_update_put(self):
        """
        PUT 메소드 테스트.
        """
        data = {
            'clothes_set': self.clothes_set,
            'start_datetime': self.start_datetime,
            'end_datetime': self.end_datetime,
            'location': self.location,
            'review': self.review,
            'comment': self.comment
        }
        url = '/clothes-set-reviews/' + str(self.created_review.id) + '/'
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_patch(self):
        """
        PATCH 메소드 테스트.
        """
        data = {
            'clothes_set': self.clothes_set,
            'start_datetime': self.start_datetime,
            'end_datetime': self.end_datetime,
            'location': self.location,
            'review': self.review,
        }
        url = '/clothes-set-reviews/' + str(self.created_review.id) + '/'
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_error_not_mine(self):
        """
        오류 - 해당 사용자의 리뷰가 아닐 시.
        """
        # Create new user.
        created_user = UserFactory.create(
            username='test-username-2',
            password=make_password('test-password'),
            nickname='test-nickname-2',
            gender='남자',
            birthday='1996-01-14'
        )
        
        # Create one clothes for new user.
        created_clothes = ClothesFactory.create(
            upper_category='상의',
            lower_category='반팔티셔츠',
            image_url='https://www.test_img.com',
            alias='test-alias',
            created_at=timezone.now(),
            owner_id=created_user.id
        )
        
        # Create one clothes set for new user.
        new_clothes_set = ClothesSetFactory.create(
            name='test-name', 
            style='화려',
            image_url='https://www.naver.com',
            created_at=timezone.now(),
            clothes=[created_clothes],
            owner=created_user
        )
        
        # Create one clothes set review for new user.
        new_review = ClothesSetReviewFactory.create(
            start_datetime=self.start_datetime, 
            end_datetime=self.end_datetime, 
            location=self.location,
            review=self.review,
            max_temp=14.3,
            min_temp=2.4,
            max_sensible_temp=13.4, 
            min_sensible_temp=0.6, 
            humidity=40,
            wind_speed=5.2,
            precipitation=4,
            comment=self.comment,
            created_at=timezone.now(),
            clothes_set_id=new_clothes_set.id,
            owner=created_user
        )
        
        data = {
            'comment': 'new comment'
        }
        url = '/clothes-set-reviews/' + str(new_review.id) + '/'
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'you are not allowed to access this object')
    
class ClothesSetReviewDeleteTests(APITestCase):
    def setUp(self):
        # Create a user and log in.
        created_user = UserFactory.create(
            username='test-username',
            password=make_password('test-password'),
            nickname='test-nickname',
            gender='남자',
            birthday='1996-01-14'
        )
        
        token_data = {
            'username': 'test-username',
            'password': 'test-password'
        }
        response = self.client.post('/api/token/', token_data, format='json')
        access_token = response.data['access']
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        
        # Create 10 Clothes for current user
        populate_clothes(10)
        
        # Create 3 ClothesSets for current user
        created_clothes_set = populate_clothes_set(3)
        
        # Create 1 ClothesSetReviews for current user
        self.created_review = populate_clothes_set_review(1)[0]
        
        self.clothes_set = created_clothes_set[0].id
        self.start_datetime = str(datetime.now() - timedelta(hours=12))
        self.start_datetime = 'T'.join(self.start_datetime.split(' '))
        self.end_datetime = str(datetime.now())
        self.end_datetime = 'T'.join(self.end_datetime.split(' '))
        self.location = 1
        self.review = 3
        self.comment = 'test-comment'
    
    def test_delete(self):
        """
        정상 삭제 테스트.
        """
        url = '/clothes-set-reviews/' + str(self.created_review.id) + '/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_error_not_mine(self):
        """
        오류 - 해당 사용자의 코디가 아닐 시.
        """
        # Create new user.
        created_user = UserFactory.create(
            username='test-username-2',
            password=make_password('test-password'),
            nickname='test-nickname-2',
            gender='남자',
            birthday='1996-01-14'
        )
        
        # Create one clothes for new user.
        created_clothes = ClothesFactory.create(
            upper_category='상의',
            lower_category='반팔티셔츠',
            image_url='https://www.test_img.com',
            alias='test-alias',
            created_at=timezone.now(),
            owner_id=created_user.id
        )
        
        # Create one clothes set for new user.
        new_clothes_set = ClothesSetFactory.create(
            name='test-name', 
            style='화려',
            image_url='https://www.naver.com',
            created_at=timezone.now(),
            clothes=[created_clothes],
            owner=created_user
        )
        
        # Create one clothes set review for new user.
        new_review = ClothesSetReviewFactory.create(
            start_datetime=self.start_datetime, 
            end_datetime=self.end_datetime, 
            location=self.location,
            review=self.review,
            max_temp=14.3,
            min_temp=2.4,
            max_sensible_temp=13.4, 
            min_sensible_temp=0.6, 
            humidity=40,
            wind_speed=5.2,
            precipitation=4,
            comment=self.comment,
            created_at=timezone.now(),
            clothes_set_id=new_clothes_set.id,
            owner=created_user
        )
        
        url = '/clothes-set-reviews/' + str(new_review.id) + '/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
class ClothesSetReviewOtherTests(APITestCase):
    def setUp(self):
        pass
    
    def test_location_search(self):
        """
        위치 검색 API 테스트.
        """
        
        response = self.client.get('/clothes-set-reviews/location_search/?search=서울특별시 종로구 청운효자동')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        
