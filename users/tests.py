from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from .models import User, Group
from rest_framework import status
from rest_framework.authtoken.models import Token

class AccountsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # URL for creating an account.
        self.sign_up_url = reverse('sign-up')
        self.sign_in_url = reverse('sign-in')
        self.create_group_url = reverse('create-group')

        # We want to go ahead and originally create a user. 
        self.credential = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        self.test_user = User.objects.create_user(**self.credential)


    def test_sign_in(self):
        """
        test sign in
        """
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }

        response = self.client.post(self.sign_in_url, data, format='json')
        user = User.objects.latest('id')
        token = Token.objects.get(user=user)
        self.assertEqual(response.data['token'], token.key)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], data['username'])
        self.assertFalse('password' in response.data)

    def test_sign_in_with_wrong_username(self):
        """
        test sign in end point with wrong username
        """
        data = {
            'username': 'wtf',
            'password': 'testpassword'
        }

        response = self.client.post(self.sign_in_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_sign_in_with_wrong_password(self):
        """
        test sign in end point with wrong username
        """
        data = {
            'username': 'testuser',
            'password': '1223asdf'
        }

        response = self.client.post(self.sign_in_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': 'somepassword',
        }

        response = self.client.post(self.sign_up_url, data, format='json')
        user = User.objects.latest('id')
        token = Token.objects.get(user=user)
        self.assertEqual(response.data['token'], token.key)

        # We want to make sure we have two users in the database..
        self.assertEqual(User.objects.count(), 2)
        # And that we're returning a 201 created code.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Additionally, we want to return the username and email upon successful creation.
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)

    def test_create_user_with_short_password(self):
        """
        Ensure user is not created for password lengths less than 8.
        """
        data = {
                'username': 'foobar',
                'email': 'foobarbaz@example.com',
                'password': 'foo'
        }

        response = self.client.post(self.sign_up_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_no_password(self):
        data = {
                'username': 'foobar',
                'email': 'foobarbaz@example.com',
                'password': ''
        }

        response = self.client.post(self.sign_up_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)



    def test_create_user_with_too_long_username(self):
        data = {
            'username': 'foo'*30,
            'email': 'foobarbaz@example.com',
            'password': 'foobarbaz'
        }

        response = self.client.post(self.sign_up_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_no_username(self):
        data = {
                'username': '',
                'email': 'foobarbaz@example.com',
                'password': 'foobarbaz'
                }

        response = self.client.post(self.sign_up_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_username(self):
        data = {
                'username': 'testuser',
                'email': 'user@example.com',
                'password': 'testuser'
                }

        response = self.client.post(self.sign_up_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)



    def test_create_user_with_preexisting_email(self):
        data = {
            'username': 'testuser2',
            'email': 'test@example.com',
            'password': 'testuser'
        }

        response = self.client.post(self.sign_up_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_invalid_email(self):
        data = {
            'username': 'foobarbaz',
            'email':  'testing',
            'passsword': 'foobarbaz'
        }

        response = self.client.post(self.sign_up_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_no_email(self):
        data = {
            'username' : 'foobar',
            'email': '',
            'password': 'foobarbaz'
        }

        response = self.client.post(self.sign_up_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_no_email_field(self):
        data = {
            'username' : 'foobar',
            'password': 'foobarbaz'
        }

        response = self.client.post(self.sign_up_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_with_no_username_field(self):
        data = {
            'email': 'foobar@example.com',
            'password': 'foobarbaz'
        }

        response = self.client.post(self.sign_up_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_create_group(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        self.client.post(self.sign_in_url, login_data, format='json')
        user = User.objects.latest('id')
        token = Token.objects.get(user=user)

        data = {
            'name': 'testgroup',
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token.key))
        response = self.client.post(self.create_group_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), 1)

    def test_create_group_with_no_name(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        self.client.post(self.sign_in_url, login_data, format='json')
        user = User.objects.latest('id')
        token = Token.objects.get(user=user)

        data = {
            'name': ''
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token.key))
        response = self.client.post(self.create_group_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Group.objects.count(), 0)
        self.assertEqual(len(response.data['name']), 1)

    def test_create_group_with_too_long_name(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        self.client.post(self.sign_in_url, login_data, format='json')
        user = User.objects.latest('id')
        token = Token.objects.get(user=user)

        data = {
            'name': 'foo'*100
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token.key))
        response = self.client.post(self.create_group_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Group.objects.count(), 0)
        self.assertEqual(len(response.data['name']), 1)

    def test_create_group_with_no_name_field(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        self.client.post(self.sign_in_url, login_data, format='json')
        user = User.objects.latest('id')
        token = Token.objects.get(user=user)
        
        data = {}

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token.key))
        response = self.client.post(self.create_group_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Group.objects.count(), 0)

    def test_create_group_with_no_token(self):
        data = {
            'name': 'testgroup',
        }

        response = self.client.post(self.create_group_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Group.objects.count(), 0)
