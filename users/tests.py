from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from .models import User, Group
from rest_framework import status

class UserTest1(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.signup_url = reverse('users:signup')
        self.signin_url = reverse('users:signin')
        self.signout_url = reverse('users:signout')
        self.group_api_url = reverse('users:group_api')

        for i in range(1, 11):
            data =  {
                'username': 'u{}'.format(i),
                'name': 'user{}'.format(i),
                'password': 'testpassword'
            }
            if i == 1:
                self.test_user = User.objects.create_user(**data)
            else:
                User.objects.create_user(**data)

        for i in range(1, 6):
            data = {
                'name': 'g{}'.format(i)
            }
            group = Group.objects.create(**data)
            group.members.add(self.test_user)

        self.client.force_authenticate(self.test_user)
            
    
    def test_signup(self):
        data = {
            'username': 'testuser',
            'name': 'jack',
            'password': 'testpassword',
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertTrue('token' in response.data)
    
    def test_signin(self):
        data = {
            'username': 'u1',
            'password': 'testpassword'
        }
        response = self.client.post(self.signin_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], data['username'])
        self.assertTrue('token' in response.data)

    def test_signout(self):
        data = {
            'username': 'u1',
            'password': 'testpassword'
        }
        self.client.post(self.signin_url, data, format='json')
        response = self.client.get(self.signout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_group(self):
        data = { 'name': 'test_group' }
        response = self.client.post(self.group_api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['members_count'], 1)
        self.assertEqual(response.data['members'][0]['username'], self.test_user.username)
        self.assertFalse('password' in response.data)
        self.assertTrue(response.data['is_joined'])



    # def test_enter_group(self):
    #     data = {
    #         'name': 'testgroup',
    #     }
    #     self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.logged_in_response.data['token']))
    #     create_res = self.client.post(self.create_group_url, data, format='json')
    #     self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Group.objects.count(), 1)
    #     self.assertEqual(len(create_res.data['members']), 1)
        
    #     regis_data = {
    #         'username': 'foobar',
    #         'email': 'foobarbaz@example.com',
    #         'password': 'foobarpassword'
    #     }
    #     user2_res = self.client.post(self.sign_up_url, regis_data, format='json')
    #     self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user2_res.data['token']))
    #     enter_res = self.client.post(reverse('enter-group', kwargs={'groupId': create_res.data['id']}))
    #     self.assertEqual(enter_res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(enter_res.data['members']), 2)
    #     self.assertEqual(enter_res.data['members'][-1]['username'], regis_data['username'])

    # def test_enter_group_with_password(self):
    #     login_data = {
    #         'cred': 'testuser',
    #         'password': 'testpassword'
    #     }
    #     user_res = self.client.post(self.sign_in_url, login_data, format='json')
    #     data = {
    #         'name': 'testgroup',
    #         'password': '1234'
    #     }
    #     self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user_res.data['token']))
    #     create_res = self.client.post(self.create_group_url, data, format='json')
    #     self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Group.objects.count(), 1)
    #     self.assertEqual(len(create_res.data['members']), 1)
        
    #     regis_data = {
    #         'username': 'foobar',
    #         'email': 'foobarbaz@example.com',
    #         'password': 'foobarpassword'
    #     }
    #     user2_res = self.client.post(self.sign_up_url, regis_data, format='json')
    #     data2 = {
    #         'password': '1234'
    #     }
    #     self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user2_res.data['token']))
    #     enter_res = self.client.post(reverse('enter-group', kwargs={'groupId': create_res.data['id']}), data2, format='json')
    #     self.assertEqual(enter_res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(enter_res.data['members']), 2)
    #     self.assertEqual(enter_res.data['members'][-1]['username'], regis_data['username'])

    # def test_enter_group_with_wrong_password(self):
    #     login_data = {
    #         'cred': 'testuser',
    #         'password': 'testpassword'
    #     }
    #     user_res = self.client.post(self.sign_in_url, login_data, format='json')
    #     data = {
    #         'name': 'testgroup',
    #         'password': '1234'
    #     }
    #     self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user_res.data['token']))
    #     create_res = self.client.post(self.create_group_url, data, format='json')
    #     self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Group.objects.count(), 1)
    #     self.assertEqual(len(create_res.data['members']), 1)
        
    #     regis_data = {
    #         'username': 'foobar',
    #         'email': 'foobarbaz@example.com',
    #         'password': 'foobarpassword'
    #     }
    #     user2_res = self.client.post(self.sign_up_url, regis_data, format='json')
    #     data2 = {
    #         'password': '123'
    #     }
    #     self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user2_res.data['token']))
    #     enter_res = self.client.post(reverse('enter-group', kwargs={'groupId': create_res.data['id']}), data2, format='json')
    #     self.assertEqual(enter_res.status_code, status.HTTP_404_NOT_FOUND)

    # def test_enter_group_with_empty_password(self):
    #     login_data = {
    #         'cred': 'testuser',
    #         'password': 'testpassword'
    #     }
    #     user_res = self.client.post(self.sign_in_url, login_data, format='json')
    #     data = {
    #         'name': 'testgroup',
    #         'password': '1234'
    #     }
    #     self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user_res.data['token']))
    #     create_res = self.client.post(self.create_group_url, data, format='json')
    #     self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Group.objects.count(), 1)
    #     self.assertEqual(len(create_res.data['members']), 1)
        
    #     regis_data = {
    #         'username': 'foobar',
    #         'email': 'foobarbaz@example.com',
    #         'password': 'foobarpassword'
    #     }
    #     user2_res = self.client.post(self.sign_up_url, regis_data, format='json')
    #     self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user2_res.data['token']))
    #     enter_res = self.client.post(reverse('enter-group', kwargs={'groupId': create_res.data['id']}), format='json')
    #     self.assertEqual(enter_res.status_code, status.HTTP_404_NOT_FOUND)

    # def test_enter_non_existing_group(self):
    #     login_data = {
    #         'cred': 'testuser',
    #         'password': 'testpassword'
    #     }
    #     user_res = self.client.post(self.sign_in_url, login_data, format='json')
    #     data = {
    #         'name': 'testgroup',
    #     }
    #     self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user_res.data['token']))
    #     create_res = self.client.post(self.create_group_url, data, format='json')
    #     self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Group.objects.count(), 1)
    #     self.assertEqual(len(create_res.data['members']), 1)
        
    #     regis_data = {
    #         'username': 'foobar',
    #         'email': 'foobarbaz@example.com',
    #         'password': 'foobarpassword'
    #     }
    #     user2_res = self.client.post(self.sign_up_url, regis_data, format='json')
    #     self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user2_res.data['token']))
    #     enter_res = self.client.post(reverse('enter-group', kwargs={'groupId': 10}))
    #     self.assertEqual(enter_res.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_leave_group(self):
    #     login_data = {
    #         'cred': 'testuser',
    #         'password': 'testpassword'
    #     }
    #     user_res = self.client.post(self.sign_in_url, login_data, format='json')
    #     data = {
    #         'name': 'testgroup',
    #     }
    #     self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user_res.data['token']))
    #     create_res = self.client.post(self.create_group_url, data, format='json')
    #     self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Group.objects.count(), 1)
    #     self.assertEqual(len(create_res.data['members']), 1)

    #     leave_res = self.client.get(reverse('leave-group', kwargs={'groupId': create_res.data['id']}))
    #     self.assertEqual(leave_res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(Group.objects.count(), 0)

    # def test_leave_non_existing_group(self):
    #     login_data = {
    #         'cred': 'testuser',
    #         'password': 'testpassword'
    #     }
    #     user_res = self.client.post(self.sign_in_url, login_data, format='json')
    #     data = {
    #         'name': 'testgroup',
    #     }
    #     self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user_res.data['token']))
    #     create_res = self.client.post(self.create_group_url, data, format='json')
    #     self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Group.objects.count(), 1)
    #     self.assertEqual(len(create_res.data['members']), 1)

    #     leave_res = self.client.get(reverse('leave-group', kwargs={'groupId': 10}))
    #     self.assertEqual(leave_res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(Group.objects.count(), 1)

    # def test_search_group(self):
    #     login_data = {
    #         'cred': 'testuser',
    #         'password': 'testpassword'
    #     }
    #     user_res = self.client.post(self.sign_in_url, login_data, format='json')
    #     data = {
    #         'name': 'testgroup',
    #     }
    #     self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user_res.data['token']))
    #     create_res = self.client.post(self.create_group_url, data, format='json')
    #     self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Group.objects.count(), 1)
    #     self.assertEqual(len(create_res.data['members']), 1)

    #     search_res = self.client.get(reverse('search-group', kwargs={'txt': 'TGr'}))
    #     self.assertEqual(search_res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(search_res.data), 1)
        
    # def test_search_group_2(self):
    #     login_data = {
    #         'cred': 'testuser',
    #         'password': 'testpassword'
    #     }
    #     user_res = self.client.post(self.sign_in_url, login_data, format='json')
    #     data = {
    #         'name': 'testgroup',
    #     }
    #     self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user_res.data['token']))
    #     create_res = self.client.post(self.create_group_url, data, format='json')
    #     self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Group.objects.count(), 1)
    #     self.assertEqual(len(create_res.data['members']), 1)

    #     search_res = self.client.get(reverse('search-group', kwargs={'txt': 'abc'}))
    #     self.assertEqual(search_res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(search_res.data), 0)
        