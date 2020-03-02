from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from .models import OriginProb, Problem
from users.models import User
from rest_framework import status

class ProbsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.add_origin_prob_url = reverse('add-origin-prob')
        self.sign_in_url = reverse('sign-in')
        self.copy_and_get_props_url = reverse('copy-and-get-probs')

        self.super_credential = {
            'username': 'root',
            'email': 'root@hmc.com',
            'password': 'asdf1488'
        }

        self.credential = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }

        self.test_superuser = User.objects.create_superuser(**self.super_credential)
        self.test_user = User.objects.create_user(**self.credential)

    def test_add_origin_prob(self):
        """
        test add original problem
        """
        user_data = {
            'username': 'root',
            'password': 'asdf1488'
        }
        user = self.client.post(self.sign_in_url, user_data, format='json')
        data = {
            'url': 'https://www.acmicpc.net/problem/1339',
            'number': 1339,
            'category': 'BOJ',
            'title': '[S/W 문제해결 기본] 8일차 - 암호문3'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user.data['token']))
        response = self.client.post(self.add_origin_prob_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OriginProb.objects.count(), 1)
        self.assertEqual(response.data['url'], data['url'])
        self.assertTrue('title' in response.data)
        self.assertTrue('url' in response.data)

    def test_add_origin_prob_by_no_admin(self):
        """
        test add original problem by non-admin user
        """
        user_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        user = self.client.post(self.sign_in_url, user_data, format='json')
        data = {
            'url': 'https://www.acmicpc.net/problem/1339',
            'number': 1339,
            'category': 'BOJ',
            'title': '[S/W 문제해결 기본] 8일차 - 암호문3'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user.data['token']))
        response = self.client.post(self.add_origin_prob_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(OriginProb.objects.count(), 0)

    def test_add_origin_prob_with_no_token(self):
        """
        test add original problem by user without token
        """
        data = {
            'url': 'https://www.acmicpc.net/problem/1339',
            'number': 1339,
            'category': 'BOJ',
            'title': '[S/W 문제해결 기본] 8일차 - 암호문3'
        }
        response = self.client.post(self.add_origin_prob_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(OriginProb.objects.count(), 0)

    def test_add_origin_prop_without_title(self):
        """
        test add original problem without title
        """
        user_data = {
            'username': 'root',
            'password': 'asdf1488'
        }
        user = self.client.post(self.sign_in_url, user_data, format='json')
        data = {
            'url': 'https://www.acmicpc.net/problem/1339',
            'number': 1339,
            'category': 'BOJ',
            # 'title': '' # ''이든 아예 키값이 없든 성공
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user.data['token']))
        response = self.client.post(self.add_origin_prob_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(OriginProb.objects.count(), 0)


    def test_add_origin_prop_without_url(self):
        """
        test add original problem without url
        """
        user_data = {
            'username': 'root',
            'password': 'asdf1488'
        }
        user = self.client.post(self.sign_in_url, user_data, format='json')
        data = {
            # 'url': 'https://www.acmicpc.net/problem/1339',
            'number': 1339,
            'category': 'BOJ',
            'title': '[S/W 문제해결 기본] 8일차 - 암호문3'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user.data['token']))
        response = self.client.post(self.add_origin_prob_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(OriginProb.objects.count(), 0)


    def test_copy_all_prob(self):
        """
        test add original problem
        """
        ### 루트를 통해 복사할 OriginProblem 넣기 (1개)
        root_data = {
            'username': 'root',
            'password': 'asdf1488'
        }
        root_res = self.client.post(self.sign_in_url, root_data, format='json')
        data = {
            'url': 'https://www.acmicpc.net/problem/1339',
            'number': 1339,
            'category': 'BOJ',
            'title': '[S/W 문제해결 기본] 8일차 - 암호문3'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(root_res.data['token']))
        response = self.client.post(self.add_origin_prob_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OriginProb.objects.count(), 1)

        ### user로 로그인 한 후, 루트의 OriginProblem을 user Problem으로 복사하고 가져오기
        user_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        user_res = self.client.post(self.sign_in_url, user_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user_res.data['token']))
        copy_response = self.client.get(self.copy_and_get_props_url)
        self.assertEqual(copy_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Problem.objects.count(), 1)
        self.assertEqual(copy_response.data[0]['origin']['url'], data['url'])
        self.assertEqual(copy_response.data[0]['origin']['number'], data['number'])
        self.assertEqual(copy_response.data[0]['origin']['title'], data['title'])


    def test_copy_same_origin(self):
        """
        test origin is copied if same probem copy
        """
        ### 루트를 통해 복사할 OriginProblem 넣기 (1개)
        root_data = {
            'username': 'root',
            'password': 'asdf1488'
        }
        root_res = self.client.post(self.sign_in_url, root_data, format='json')
        data = {
            'url': 'https://www.acmicpc.net/problem/1339',
            'number': 1339,
            'category': 'BOJ',
            'title': '[S/W 문제해결 기본] 8일차 - 암호문3'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(root_res.data['token']))
        response = self.client.post(self.add_origin_prob_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OriginProb.objects.count(), 1)

        ### user로 로그인 한 후, 루트의 OriginProblem을 user Problem으로 복사하고 가져오기
        user_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        user_res = self.client.post(self.sign_in_url, user_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(user_res.data['token']))
        copy_response = self.client.get(self.copy_and_get_props_url)
        self.assertEqual(copy_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Problem.objects.count(), 1)

        copy_response = self.client.get(self.copy_and_get_props_url)
        self.assertEqual(copy_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Problem.objects.count(), 1)