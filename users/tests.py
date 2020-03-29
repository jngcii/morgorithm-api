from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from .models import User, Group
from rest_framework import status
from rest_framework.authtoken.models import Token
# import pprint

class AccountsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # URL for creating an account.
        self.sign_up_url = reverse('sign-up')
        self.sign_in_url = reverse('sign-in')
        self.change_password_url = reverse('change-password')
        self.send_confirm_code_url = reverse('send-confirm-code')
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

        # pprint.pprint(response.data)

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

    def test_change_password(self):
        user_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }

        login_res = self.client.post(self.sign_in_url, user_data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(login_res.status_code, status.HTTP_200_OK)

        data = {
            'old_password': 'testpassword',
            'new_password': 'mypassword'
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(login_res.data['token']))
        change_res = self.client.post(self.change_password_url, data, format='json')
        self.assertEqual(change_res.status_code, status.HTTP_200_OK)

    def test_change_password_with_too_short_password(self):
        user_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }

        login_res = self.client.post(self.sign_in_url, user_data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(login_res.status_code, status.HTTP_200_OK)

        data = {
            'old_password': 'testpassword',
            'new_password': 'pw'
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(login_res.data['token']))
        change_res = self.client.post(self.change_password_url, data, format='json')
        self.assertEqual(change_res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_with_too_long_password(self):
        user_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }

        login_res = self.client.post(self.sign_in_url, user_data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(login_res.status_code, status.HTTP_200_OK)

        data = {
            'old_password': 'testpassword',
            'new_password': 'password'*20
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(login_res.data['token']))
        change_res = self.client.post(self.change_password_url, data, format='json')
        self.assertEqual(change_res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_with_wrong_password(self):
        user_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }

        login_res = self.client.post(self.sign_in_url, user_data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(login_res.status_code, status.HTTP_200_OK)

        data = {
            'old_password': 'pw',
            'new_password': 'password'
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(login_res.data['token']))
        change_res = self.client.post(self.change_password_url, data, format='json')
        self.assertEqual(change_res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_with_no_field(self):
        user_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }

        login_res = self.client.post(self.sign_in_url, user_data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(login_res.status_code, status.HTTP_200_OK)

        data = {}

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(login_res.data['token']))
        change_res = self.client.post(self.change_password_url, data, format='json')
        self.assertEqual(change_res.status_code, status.HTTP_400_BAD_REQUEST)

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

    def test_send_confirm_code(self):
        data = {
            'email': 'eeeee@example.com',
        }
        response = self.client.post(self.send_confirm_code_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['confirm_code']), 8)
        self.assertEqual(User.objects.latest('id').is_confirmed, False)

    def test_create_group(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        user_res = self.client.post(self.sign_in_url, login_data, format='json')
        data = {
            'name': 'testgroup',
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user_res.data['token']))
        response = self.client.post(self.create_group_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(len(response.data['members']), 1)
        self.assertTrue('members_count' in response.data)

    def test_create_group_with_password(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        user_res = self.client.post(self.sign_in_url, login_data, format='json')
        data = {
            'name': 'testgroup',
            'password': '1234'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user_res.data['token']))
        response = self.client.post(self.create_group_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(len(response.data['members']), 1)
        self.assertFalse('password' in response.data)


    def test_create_group_with_too_long_password(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        user_res = self.client.post(self.sign_in_url, login_data, format='json')
        data = {
            'name': 'testgroup',
            'password': '1234123412341234'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user_res.data['token']))
        response = self.client.post(self.create_group_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Group.objects.count(), 0)


    def test_create_group_with_no_name(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        user_res = self.client.post(self.sign_in_url, login_data, format='json')
        data = {
            'name': ''
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user_res.data['token']))
        response = self.client.post(self.create_group_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Group.objects.count(), 0)
        self.assertEqual(len(response.data['name']), 1)

    def test_create_group_with_too_long_name(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        user_res = self.client.post(self.sign_in_url, login_data, format='json')
        data = {
            'name': 'foo'*100
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user_res.data['token']))
        response = self.client.post(self.create_group_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Group.objects.count(), 0)
        self.assertEqual(len(response.data['name']), 1)

    def test_create_group_with_no_name_field(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        user_res = self.client.post(self.sign_in_url, login_data, format='json')
        data = {}
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user_res.data['token']))
        response = self.client.post(self.create_group_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Group.objects.count(), 0)
        self.assertEqual(len(response.data['name']), 1)

    def test_create_group_with_no_token(self):
        data = {
            'name': 'testgroup',
        }
        response = self.client.post(self.create_group_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Group.objects.count(), 0)

    def test_enter_group(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        user_res = self.client.post(self.sign_in_url, login_data, format='json')
        data = {
            'name': 'testgroup',
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user_res.data['token']))
        create_res = self.client.post(self.create_group_url, data, format='json')
        self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(len(create_res.data['members']), 1)
        
        regis_data = {
            'username': 'foobar',
            'email': 'foobarbaz@example.com',
            'password': 'foobarpassword'
        }
        user2_res = self.client.post(self.sign_up_url, regis_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user2_res.data['token']))
        enter_res = self.client.post(reverse('enter-group', kwargs={'groupId': create_res.data['id']}))
        self.assertEqual(enter_res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(enter_res.data['members']), 2)
        self.assertEqual(enter_res.data['members'][-1]['username'], regis_data['username'])

    def test_enter_group_with_password(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        user_res = self.client.post(self.sign_in_url, login_data, format='json')
        data = {
            'name': 'testgroup',
            'password': '1234'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user_res.data['token']))
        create_res = self.client.post(self.create_group_url, data, format='json')
        self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(len(create_res.data['members']), 1)
        
        regis_data = {
            'username': 'foobar',
            'email': 'foobarbaz@example.com',
            'password': 'foobarpassword'
        }
        user2_res = self.client.post(self.sign_up_url, regis_data, format='json')
        data2 = {
            'password': '1234'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user2_res.data['token']))
        enter_res = self.client.post(reverse('enter-group', kwargs={'groupId': create_res.data['id']}), data2, format='json')
        self.assertEqual(enter_res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(enter_res.data['members']), 2)
        self.assertEqual(enter_res.data['members'][-1]['username'], regis_data['username'])

    def test_enter_group_with_wrong_password(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        user_res = self.client.post(self.sign_in_url, login_data, format='json')
        data = {
            'name': 'testgroup',
            'password': '1234'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user_res.data['token']))
        create_res = self.client.post(self.create_group_url, data, format='json')
        self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(len(create_res.data['members']), 1)
        
        regis_data = {
            'username': 'foobar',
            'email': 'foobarbaz@example.com',
            'password': 'foobarpassword'
        }
        user2_res = self.client.post(self.sign_up_url, regis_data, format='json')
        data2 = {
            'password': '123'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user2_res.data['token']))
        enter_res = self.client.post(reverse('enter-group', kwargs={'groupId': create_res.data['id']}), data2, format='json')
        self.assertEqual(enter_res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_enter_group_with_empty_password(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        user_res = self.client.post(self.sign_in_url, login_data, format='json')
        data = {
            'name': 'testgroup',
            'password': '1234'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user_res.data['token']))
        create_res = self.client.post(self.create_group_url, data, format='json')
        self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(len(create_res.data['members']), 1)
        
        regis_data = {
            'username': 'foobar',
            'email': 'foobarbaz@example.com',
            'password': 'foobarpassword'
        }
        user2_res = self.client.post(self.sign_up_url, regis_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user2_res.data['token']))
        enter_res = self.client.post(reverse('enter-group', kwargs={'groupId': create_res.data['id']}), format='json')
        self.assertEqual(enter_res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_enter_non_existing_group(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        user_res = self.client.post(self.sign_in_url, login_data, format='json')
        data = {
            'name': 'testgroup',
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user_res.data['token']))
        create_res = self.client.post(self.create_group_url, data, format='json')
        self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(len(create_res.data['members']), 1)
        
        regis_data = {
            'username': 'foobar',
            'email': 'foobarbaz@example.com',
            'password': 'foobarpassword'
        }
        user2_res = self.client.post(self.sign_up_url, regis_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user2_res.data['token']))
        enter_res = self.client.post(reverse('enter-group', kwargs={'groupId': 10}))
        self.assertEqual(enter_res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_leave_group(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        user_res = self.client.post(self.sign_in_url, login_data, format='json')
        data = {
            'name': 'testgroup',
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user_res.data['token']))
        create_res = self.client.post(self.create_group_url, data, format='json')
        self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(len(create_res.data['members']), 1)

        leave_res = self.client.get(reverse('leave-group', kwargs={'groupId': create_res.data['id']}))
        self.assertEqual(leave_res.status_code, status.HTTP_200_OK)
        self.assertEqual(Group.objects.count(), 0)

    def test_leave_non_existing_group(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        user_res = self.client.post(self.sign_in_url, login_data, format='json')
        data = {
            'name': 'testgroup',
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user_res.data['token']))
        create_res = self.client.post(self.create_group_url, data, format='json')
        self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(len(create_res.data['members']), 1)

        leave_res = self.client.get(reverse('leave-group', kwargs={'groupId': 10}))
        self.assertEqual(leave_res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Group.objects.count(), 1)

    def test_search_group(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        user_res = self.client.post(self.sign_in_url, login_data, format='json')
        data = {
            'name': 'testgroup',
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user_res.data['token']))
        create_res = self.client.post(self.create_group_url, data, format='json')
        self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(len(create_res.data['members']), 1)

        search_res = self.client.get(reverse('search-group', kwargs={'txt': 'TGr'}))
        self.assertEqual(search_res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(search_res.data), 1)
        
    def test_search_group_2(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        user_res = self.client.post(self.sign_in_url, login_data, format='json')
        data = {
            'name': 'testgroup',
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user_res.data['token']))
        create_res = self.client.post(self.create_group_url, data, format='json')
        self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(len(create_res.data['members']), 1)

        search_res = self.client.get(reverse('search-group', kwargs={'txt': 'abc'}))
        self.assertEqual(search_res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(search_res.data), 0)
        