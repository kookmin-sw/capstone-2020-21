from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.api.factories import (
    UserFactory,
    ClothesFactory,
    ClothesSetFactory
)
from apps.api.populate import populate_clothes, populate_clothes_set

class ClohtesSetCreateTests(APITestCase):
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
    
        self.clothes = [1,2,3,4,5]
        self.name = 'test-name'
        self.style = '화려'
        self.image_url = 'https://www.naver.com'
    
    def test_create(self):
        """
        정상생성 테스트.
        """
        data = {
            'clothes': self.clothes,
            'name': self.name,
            'style': self.style,
            'image_url': self.image_url
        }
        response = self.client.post('/clothes-sets/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['clothes'], self.clothes)
        self.assertEqual(response.data['name'], self.name)
        self.assertEqual(response.data['style'], self.style)
        self.assertEqual(response.data['image_url'], self.image_url)
    
    def test_create_required(self):
        """
        필수필드생성 테스트.
        """
        data = {
            'clothes': self.clothes,
            'image_url': self.image_url
        }
        response = self.client.post('/clothes-sets/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['clothes'], self.clothes)
        self.assertEqual(response.data['image_url'], self.image_url)
    
    def test_create_error_no_required(self):
        """
        오류 - 필수 필드 없을 경우.
        """
        data = {}
        response = self.client.post('/clothes-sets/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['clothes'][0], 'This field is required.')
        self.assertEqual(response.data['image_url'][0], 'This field is required.')
    
    def test_create_error_authentication(self):
        """
        오류 - 인증정보 오류.
        """
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.post('/clothes-sets/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")

class ClothesSetRetrieveTests(APITestCase):
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
        populate_clothes_set(3)
    
        self.clothes = [1,2,3,4,5]
        self.name = 'test-name'
        self.style = '화려'
        self.image_url = 'https://www.naver.com'
        
    def test_retrieve_one(self):
        """
        단일 코디 정보 반환 테스트.
        """
        response = self.client.get('/clothes-sets/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_retrieve_many(self):
        """
        여러 개 코디 정보 반환 테스트.
        """
        response = self.client.get('/clothes-sets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        
    def test_retrieve_me(self):
        """
        내 코디 정보 반환 테스트.
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
            owner_id=2
        )
        
        # Create one clothes set for new user.
        ClothesSetFactory.create(
            name=self.name, 
            style=self.style,
            image_url=self.image_url,
            created_at=timezone.now(),
            clothes=[created_clothes],
            owner=created_user
        )
        
        # Total Clothe sets : 4.
        response = self.client.get('/clothes-sets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 4)
        
        # Current User's Clothes sets : 3.
        response = self.client.get('/clothes-sets/?me=True')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
    
class ClothesSetUpdateTests(APITestCase):
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
        
        # Create 1 ClothesSets for current user
        populate_clothes_set(1)
    
        self.clothes = [1,2,3,4,5]
        self.name = 'test-name'
        self.style = '화려'
        self.image_url = 'https://www.naver.com'
    
    def test_update_put(self):
        """
        PUT 메소드 테스트.
        """
        data = {
            'clothes': self.clothes,
            'name': self.name,
            'style': self.style,
            'image_url': self.image_url
        }
        response = self.client.put('/clothes-sets/1/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['clothes'], self.clothes)
        self.assertEqual(response.data['name'], self.name)
        self.assertEqual(response.data['style'], self.style)
        self.assertEqual(response.data['image_url'], self.image_url)
    
    def test_update_patch(self):
        """
        PATCH 메소드 테스트.
        """
        new_name = 'test-name-new'
        data = {
            'name': new_name
        }
        response = self.client.patch('/clothes-sets/1/', data, format='json')
        self.assertEqual(response.data['name'], new_name)
    
    def test_update_error_not_mine(self):
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
            owner_id=2
        )
        
        # Create one clothes set for new user.
        ClothesSetFactory.create(
            name=self.name, 
            style=self.style,
            image_url=self.image_url,
            created_at=timezone.now(),
            clothes=[created_clothes],
            owner=created_user
        )
        
        data = {
            'name': 'new_name'
        }
        response = self.client.patch('/clothes-sets/2/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'you are not allowed to access this object')
    
class ClothesSetDeleteTests(APITestCase):
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
        
        # Create 1 ClothesSets for current user
        populate_clothes_set(1)
    
    def test_delete(self):
        """
        정상 삭제 테스트.
        """
        response = self.client.delete('/clothes-sets/1/')
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
            image_url='https://www.naver.com',
            alias='test-alias',
            created_at=timezone.now(),
            owner_id=2
        )
        
        # Create one clothes set for new user.
        ClothesSetFactory.create(
            name='test-name', 
            style='화려',
            image_url='https://www.naver.com',
            created_at=timezone.now(),
            clothes=[created_clothes],
            owner=created_user
        )
        
        response = self.client.delete('/clothes-sets/2/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
