from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.api.factories import UserFactory, ClothesFactory
from apps.api.populate import populate_clothes

class ClohtesCreateTests(APITestCase):
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
        
        self.alias = 'test-alias'
        with open("temp/sample_image.png", 'rb') as image:
            self.image = image.read()
            
    def test_create(self):
        """
        정상생성 테스트.
        """
        data = self.image
        response = self.client.post('/clothes/inference/', data, content_type='image/png')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        image_url = response.data['image_url']
        upper_category = response.data['upper_category']
        lower_category = response.data['lower_category']
        
        data = {
            'image_url': image_url,
            'upper_category': upper_category,
            'lower_category': lower_category,
            'alias': self.alias
        }
        response = self.client.post('/clothes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['upper_category'], upper_category)
        self.assertEqual(response.data['lower_category'], lower_category)
        self.assertEqual(response.data['alias'], self.alias)
        
    
    def test_create_required(self):
        """
        필수필드생성 테스트.
        """
        data = self.image
        response = self.client.post('/clothes/inference/', data, content_type='image/png')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        image_url = response.data['image_url']
        upper_category = response.data['upper_category']
        lower_category = response.data['lower_category']
        
        data = {
            'image_url': image_url,
            'upper_category': upper_category,
            'lower_category': lower_category,
        }
        response = self.client.post('/clothes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['upper_category'], upper_category)
        self.assertEqual(response.data['lower_category'], lower_category)
    
    def test_create_error_no_required(self):
        """
        오류 - 필수 필드 없을 경우.
        """
        data = {}
        response = self.client.post('/clothes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['image_url'][0], 'This field is required.')
        self.assertEqual(response.data['lower_category'][0], 'This field is required.')
        self.assertEqual(response.data['upper_category'][0], 'This field is required.')
    
    def test_create_error_wrong_image_url(self):
        """
        오류 - 이미지 URL 잘못된 경우.
        """
        data = {
            'image_url': 'https://otte-bucket.s3.ap-northeast-2.amazonaws.com/clothes/temp/clothes_1385906387893.png',
            'upper_category': '상의',
            'lower_category': '반팔티셔츠'
        }
        response = self.client.post('/clothes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'image does not exist ... plesase try again')
    
    def test_create_error_authentication(self):
        """
        오류 - 인증정보 오류.
        """
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.post('/clothes/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")
        

class ClothesRetrieveTests(APITestCase):
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
        
        # Create 10 Clothes for test.
        populate_clothes(10)
        
    def test_retrieve_one(self):
        """
        단일 옷 정보 반환 테스트.
        """
        response = self.client.get('/clothes/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_retrieve_many(self):
        """
        여러 개 옷 정보 반환 테스트.
        """
        response = self.client.get('/clothes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 10)
        
    def test_retrieve_me(self):
        # Create new user.
        UserFactory.create(
            username='test-username-2',
            password=make_password('test-password'),
            nickname='test-nickname-2',
            gender='남자',
            birthday='1996-01-14'
        )
        
        # Create one clothes for new user.
        ClothesFactory.create(
            upper_category='상의',
            lower_category='반팔티셔츠',
            image_url='https://www.test_img.com',
            alias='test-alias',
            created_at=timezone.now(),
            owner_id=2
        )
        
        # Total clothes : 11.
        response = self.client.get('/clothes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 11)
        
        # Current User's clothes : 10.
        response = self.client.get('/clothes/?me=True')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 10)
        
    
class ClothesUpdateTests(APITestCase):
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
        
        # Create 1 Clothes for test.
        populate_clothes(1)
        
        self.upper_category='상의'
        self.lower_category='반팔티셔츠'
        self.image_url='https://www.naver.com'
        self.alias='test-alias'
    
    def test_update_put(self):
        """
        PUT 메소드 테스트.
        """
        data = {
            'upper_category': self.upper_category,
            'lower_category': self.lower_category,
            'image_url': self.image_url,
            'alias': self.alias,
        }
        response = self.client.put('/clothes/1/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['upper_category'], self.upper_category)
        self.assertEqual(response.data['lower_category'], self.lower_category)
        self.assertEqual(response.data['image_url'], self.image_url)
        self.assertEqual(response.data['alias'], self.alias)
    
    def test_update_patch(self):
        """
        PATCH 메소드 테스트.
        """
        data = {
            'alias': self.alias,
        }
        response = self.client.patch('/clothes/1/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['alias'], self.alias)
    
    def test_update_error_not_mine(self):
        """
        오류 - 해당 사용자의 옷이 아닐 시.
        """
        # Create new user.
        UserFactory.create(
            username='test-username-2',
            password=make_password('test-password'),
            nickname='test-nickname-2',
            gender='남자',
            birthday='1996-01-14'
        )
        
        # Create one clothes for new user.
        ClothesFactory.create(
            upper_category='상의',
            lower_category='반팔티셔츠',
            image_url='https://www.test_img.com',
            alias='test-alias',
            created_at=timezone.now(),
            owner_id=2
        )
        
        data = {
            'alias': self.alias,
        }
        response = self.client.patch('/clothes/2/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'you are not allowed to access this object')
        
    
class ClothesDeleteTests(APITestCase):
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
        
        # Create 1 Clothes for test.
        populate_clothes(1)
    
    def test_delete(self):
        """
        정상 삭제 테스트.
        """
        response = self.client.delete('/clothes/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_error_not_mine(self):
        """
        오류 - 해당 사용자의 옷이 아닐 시.
        """
        # Create new user.
        UserFactory.create(
            username='test-username-2',
            password=make_password('test-password'),
            nickname='test-nickname-2',
            gender='남자',
            birthday='1996-01-14'
        )
        
        # Create one clothes for new user.
        ClothesFactory.create(
            upper_category='상의',
            lower_category='반팔티셔츠',
            image_url='https://www.naver.com',
            alias='test-alias',
            created_at=timezone.now(),
            owner_id=2
        )
        
        response = self.client.delete('/clothes/2/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'you are not allowed to access this object')
    
