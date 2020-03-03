from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from .models import Solution
from users.models import User
from rest_framework import status
from pprint import pprint

class SolutionTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.sign_up_url = reverse('sign-up')
        self.sign_in_url = reverse('sign-in')
        self.add_origin_prob_url = reverse('add-origin-prob')
        self.copy_and_get_props_url = reverse('copy-and-get-probs')
        self.add_solution_url = reverse('add-solution')

        self.super_credential = {
            'username': 'root',
            'email': 'root@hmc.com',
            'password': 'asdf1488'
        }
        self.super_user_data = {
            'username': 'root',
            'password': 'asdf1488'
        }

        self.credential = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }

        User.objects.create_superuser(**self.super_credential)
        User.objects.create_user(**self.credential)

        self.test_superuser = self.client.post(self.sign_in_url, self.super_user_data, format='json')
        self.test_user = self.client.post(self.sign_in_url, self.user_data, format='json')

        self.origin_prob_data = {
            'url': 'https://www.acmicpc.net/problem/1339',
            'number': 1339,
            'category': 'BOJ',
            'title': '[S/W 문제해결 기본] 8일차 - 암호문3'
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.test_superuser.data['token']))
        self.client.post(self.add_origin_prob_url, self.origin_prob_data, format='json')

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.test_user.data['token']))
        self.copy_res = self.client.get(self.copy_and_get_props_url)

        self.assertEqual(self.copy_res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.copy_res.data[0]['origin']['url'], self.origin_prob_data['url'])

    def test_add_solved_solution(self):
        # print(self.copy_res.data[0]['origin'])
        """
        test adding solved solution
        """
        data = {
            'problem': self.copy_res.data[0]['origin']['id'],
            'code': """def add(a, b):
            return a + b
            """,
            'lang': 'python',
            'solved': True
        }

        response = self.client.post(self.add_solution_url, data, format='json')
        # pprint(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Solution.objects.count(), 1)
        self.assertEqual(response.data['view'], 0)
        self.assertFalse(response.data['caption'])

    def test_add_unsolved_solution(self):
        # print(self.copy_res.data[0]['origin'])
        """
        test adding unsolved solution
        """
        data = {
            'problem': self.copy_res.data[0]['origin']['id'],
            'code': """def add(a, b):
            return a + b
            """,
            'caption': '뭐가 틀린지 모르겠어요.',
            'lang': 'python',
            'solved': False
        }

        response = self.client.post(self.add_solution_url, data, format='json')
        # pprint(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Solution.objects.count(), 1)
        self.assertEqual(response.data['view'], 0)
        self.assertEqual(response.data['caption'], data['caption'])