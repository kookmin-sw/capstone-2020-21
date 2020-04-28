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
        self.gender = '남자'
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
        token_data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post('/api/token/', token_data, format='json')
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
        self.assertEqual(response.data['nickname'][0], 'This field is required.')
        self.assertEqual(response.data['gender'][0], 'This field is required.')
        
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
        self.assertEqual(str(response.data['nickname'][0]), "user with this nickname already exists.")


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
        self.gender = '남자'
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
        response = self.client.post('/api/token/', token_data, format='json')
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
        response = self.client.get('/users/' + str(self.created_user['id']) + '/')
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
        
    def test_me_query_fail(self):
        url = reverse('users-me')
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")
        
    def test_login_failure(self):
        """
        Check if login fail message is returned.
        """
        # Set credentials.
        self.client.credentials(HTTP_AUTHORIZATION='')
        
        token_data = {
            'username': self.username,
            'password': 'wrong-password'
        }
        response = self.client.post('/api/token/', token_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'No active account found with the given credentials')
        

class UserUpdateTests(APITestCase):
    def setUp(self):
        """
        Sets up username, password, nickname, gender, birthday,
        created_user, credentials for self.client.
        Creates one user.
        """
        self.username = 'test-user'
        self.password = 'test-password'
        self.nickname = 'test-nickname'
        self.gender = '남자'
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
        response = self.client.post('/api/token/', token_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data['access']
        
        # Set credentials.
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    
    def test_update_user_full(self):
        username = 'new_username'
        password = 'new_password'
        nickname = 'new_nickname'
        gender = '여자'
        birthday = '2000-01-01'
        
        data = {
            'username': username,
            'password': password,
            'nickname': nickname,
            'gender': gender, 
            'birthday': birthday
        }
        
        url = '/users/' + str(self.created_user['id']) + '/'
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.data['username'], username)
        self.assertEqual(response.data['nickname'], nickname)
        self.assertEqual(response.data['gender'], gender)
        self.assertEqual(response.data['birthday'], birthday)
        
    def test_update_user_partial(self):
        nickname = 'new_nickname'
        gender = '여자'
        birthday = '2000-01-01'
        
        data = {
            'nickname': nickname,
            'gender': gender, 
            'birthday': birthday
        }
        url = '/users/' + str(self.created_user['id']) + '/'
        
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.data['username'], self.username)
        self.assertEqual(response.data['nickname'], nickname)
        self.assertEqual(response.data['gender'], gender)
        self.assertEqual(response.data['birthday'], birthday)

    def test_update_user_duplicate_name(self):
        username = 'test-user-dup'
        nickname = 'test-user-dup'
        
        # Create user for test.
        url = reverse('users-list')
        data = {
            'username': username,
            'password': self.password,
            'nickname': nickname,
            'gender': self.gender, 
            'birthday': self.birthday
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        data = {
            'username': username,
            'nickname': nickname
        }
         
        url = '/users/' + str(self.created_user['id']) + '/'
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['username'][0]), 'user with this username already exists.')
        self.assertEqual(str(response.data['nickname'][0]), 'user with this nickname already exists.')
        
    def test_update_not_authorized(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        
        username = 'new_username'
        password = 'new_password'
        nickname = 'new_nickname'
        gender = '여자'
        birthday = '2000-01-01'
        
        data = {
            'username': username,
            'password': password,
            'nickname': nickname,
            'gender': gender, 
            'birthday': birthday
        }
        
        url = '/users/' + str(self.created_user['id']) + '/'
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
    
    def test_update_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        
        username = 'new_username'
        password = 'new_password'
        nickname = 'new_nickname'
        gender = '여자'
        birthday = '2000-01-01'
        
        data = {
            'username': username,
            'password': password,
            'nickname': nickname,
            'gender': gender, 
            'birthday': birthday
        }
        
        response = self.client.put('/users/1/', data, format='json')
        self.assertEqual(response.data['detail'], 'Given token not valid for any token type')
        
class UserDeleteTests(APITestCase):
    def setUp(self):
        """
        Sets up username, password, nickname, gender, birthday,
        created_user, credentials for self.client.
        Creates one user.
        """
        self.username = 'test-user'
        self.password = 'test-password'
        self.nickname = 'test-nickname'
        self.gender = '남자'
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
        response = self.client.post('/api/token/', token_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data['access']
        
        # Set credentials.
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        
    def test_delete_existing_user(self):
        response = self.client.delete('/users/1')
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)
        
    def test_delete_non_existing_user(self):
        response = self.client.delete('/users/2')
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)

    def test_delete_not_authorized(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        
        response = self.client.delete('/users/1/')
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
    
    def test_update_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        
        response = self.client.delete('/users/2/')
        self.assertEqual(response.data['detail'], 'Given token not valid for any token type')

