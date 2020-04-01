from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User

class UserCreateTests(APITestCase):
    def test_create_user_success(self):
        """
        test if creating user works in successful conditions
        """
        url = reverse('users-list')
        data = {
            'username': 'test-user',
            'password': 'test-password',
            'nickname': 'test-nickname',
            'gender': True, 
            'birthday': '1996-01-04'
        }
        
        # Create Account.
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'test-user')
        self.assertEqual(response.data['nickname'], 'test-nickname')
        self.assertEqual(response.data['gender'], True)
        self.assertEqual(response.data['birthday'], '1996-01-04')
        
        # Check Login.
        token_url = reverse('token_obtain_pair')
        token_data = {
            'username': 'test-user',
            'password': 'test-password'
        }
        response = self.client.post('/api/token/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_user_partial(self):
        """
        test if creating user works when partial data is given
        """
        url = reverse('users-list')
        data = {
            'username': 'test-user',
            'password': 'test-password',
        }
        
        # Create Account.
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'test-user')
        self.assertEqual(response.data['nickname'], '닉네임을 입력해주세요.')
        self.assertEqual(response.data['gender'], True)
        self.assertEqual(response.data['birthday'], None)
        
        # Check Login.
        token_url = reverse('token_obtain_pair')
        token_data = {
            'username': 'test-user',
            'password': 'test-password'
        }
        response = self.client.post('/api/token/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_failure(self):
        """
        test if creating user gives error message in unsuccessful conditions
        """
        url = reverse('users-list')
        data = {
            'username': 'test-user',
        }
        
        # Create account only w/ username.
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password'][0], 'This field is required.')

        data = {
            'passsword': 'test-password',
        }
        
        # Create account only w/ password.
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['username'][0], 'This field is required.')
        
    def test_create_user_duplicate_username(self):
        """
        test if creating user gives error message
        when duplicate username is given
        """
        url = reverse('users-list')
        data = {
            'username': 'test-user',
            'password': 'test-password',
            'nickname': 'test-nickname',
            'gender': True, 
            'birthday': '1996-01-04'
        }
        
        # Create account 1.
        response = self.client.post(url, data, format='json')

        data = {
            'username': 'test-user',
            'password': 'test-password2',
            'nickname': 'test-nickname2',
            'gender': True, 
            'birthday': '1996-01-04'
        }
        # Create account 2, w/ duplicate username
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['username'][0]), "user with this username already exists.")
        
