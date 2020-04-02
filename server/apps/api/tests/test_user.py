from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate

from apps.api.models import User
from apps.api.factories import UserFactory

class UserCreateTests(APITestCase):
    def setUp(self):
        """
        Sets up username, password, nickname, gender, birthday.
        """
        self.username = 'test-user'
        self.password = 'test-password'
        self.nickname = 'test-nickname'
        # TODO(mskwon1): change this to '남자' or '여자'.
        self.gender = True
        self.birthday = '1996-01-14'        
        
    def test_create_user_success(self):
        """
        test if creating user works in successful conditions.
        """        
        url = reverse('users-list')
        data = {
            'username': self.username,
            'password': self.password,
            'nickname': self.nickname,
            'gender': self.gender, 
            'birthday': self.birthday
        }
        
        # Create Account.
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotContains(response, 'password', status_code=status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], self.username)
        self.assertEqual(response.data['nickname'], self.nickname)
        self.assertEqual(response.data['gender'], self.gender)
        self.assertEqual(response.data['birthday'], self.birthday)
        
        # Check Login.
        token_url = reverse('token_obtain_pair')
        token_data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post('/api/token/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_user_required(self):
        """
        test if creating user works when only required data is given.
        """
        url = reverse('users-list')
        data = {
            'username': self.username,
            'password': self.password,
            'nickname': self.nickname,
            'gender': self.gender,
        }
        
        # Create Account.
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotContains(response, 'password', status_code=status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], self.username)
        self.assertEqual(response.data['nickname'], self.nickname)
        self.assertEqual(response.data['gender'], self.gender)
        self.assertEqual(response.data['birthday'], None)
        
        # Check Login.
        token_url = reverse('token_obtain_pair')
        token_data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post('/api/token/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'access', status_code=status.HTTP_200_OK)
        self.assertContains(response, 'refresh', status_code=status.HTTP_200_OK)

    def test_create_user_failure(self):
        """
        test if creating user gives error message in unsuccessful conditions.
        """
        url = reverse('users-list')
        data = {}
        
        # Create account only w/ empty body.
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['username'][0], 'This field is required.')
        self.assertEqual(response.data['password'][0], 'This field is required.')
        # TODO(mskwon1): Enable this.
        # self.assertEqual(response.data['nickname'][0], 'This field is required.')
        # self.assertEqual(response.data['gender'][0], 'This field is required.')
        
    def test_create_user_duplicate_username(self):
        """
        test if creating user gives error message
        when duplicate username/nickname is given.
        """
        url = reverse('users-list')
        data = {
            'username': self.username,
            'password': self.password,
            'nickname': self.nickname,
            'gender': self.gender, 
            'birthday': self.birthday
        }
        
        # Create account 1.
        response = self.client.post(url, data, format='json')
        
        # Create account 2, w/ duplicate username & nickname
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['username'][0]), "user with this username already exists.")
        # TODO(mskwon1): Enable this.
        # self.assertEqual(str(response.data['nickname'][0]), "user with this nickname already exists.")


class UserRetrieveTests(APITestCase):
    def setUp(self):
        """
        Sets up username, password, nickname, gender, birthday,
        created_user, credentials for self.client.
        Creates one user.
        """
        self.username = 'test-user'
        self.password = 'test-password'
        self.nickname = 'test-nickname'
        # TODO(mskwon1): change this to '남자' or '여자'.
        self.gender = True
        self.birthday = '1996-01-14'
        
        # Create user for test.
        url = reverse('users-list')
        data = {
            'username': self.username,
            'password': self.password,
            'nickname': self.nickname,
            'gender': self.gender, 
            'birthday': self.birthday
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.created_user = response.data
        
        # Log the user in.
        token_data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post('/api/token/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data['access']
        
        # Set credentials.
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    
    def test_existing_user(self):
        # Test list view.
        url = reverse('users-list')
        response = self.client.get(url)
        self.assertEqual(int(response.data['count']), 1)

        # Test detail view.
        response = self.client.get('/users/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.created_user)
    
    def test_non_existing_user(self):
        # Test detail view.
        response = self.client.get('/users/2/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_me_query(self):
        url = reverse('users-me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.created_user)