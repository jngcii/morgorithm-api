from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from .models import OriginProb, Problem
from users.models import User
from rest_framework import status
# from pprint import pprint

class ProblemTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.get_problem_list_url = reverse('problems:get_problem_list')
        self.fetch_url = reverse('problems:fetch')
        self.init_url = reverse('problems:init')
        self.problem_group_api_url = reverse('problems:problem_group_api')

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
        self.client.force_authenticate(user=self.test_user)

        for i in range(1, 11):
            data = {
                'url': 'https://www.acmicpc.net/problem/{}'.format(i),
                'number': i,
                'category': 'BOJ',
                'title': 'test {}'.format(i)
            }
            OriginProb.objects.create(**data)
    

    def test_fetch(self):
        data = {
            'url': 'https://www.acmicpc.net/problem/11',
            'number': 11,
            'category': 'BOJ',
            'title': 'test 11'
        }
        response = self.client.post(self.fetch_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['url'], data['url'])

    def test_init(self):
        data = {
            'url': 'https://www.acmicpc.net/problem/11',
            'number': 11,
            'category': 'BOJ',
            'title': 'test 11'
        }
        # 새로 가입한 사람이 init
        response = self.client.get(self.init_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)
        self.assertEqual(Problem.objects.count(), 10)
        # 새로운 문제 업데이트 전에 init
        response2 = self.client.get(self.init_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(response2.data))
        # 새로운 문제 업데이트 후 첫 init
        self.client.post(self.fetch_url, data, format='json')
        response3 = self.client.get(self.init_url)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(response3.data)-1)

    def test_get_problem_list(self):
        self.client.get(self.init_url)
        response = self.client.post(self.get_problem_list_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertEqual(response.data['results'][0]['origin']['number'], 1)
        self.assertTrue('origin' in response.data['results'][0])
        self.assertTrue('is_solved' in response.data['results'][0])

    def test_get_problem_list_2(self):
        self.client.get(self.init_url)
        response = self.client.post('/api/v1/probs/?limit=5&offset=5', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertEqual(response.data['results'][0]['origin']['number'], 6)
        self.assertTrue('origin' in response.data['results'][0])
        self.assertTrue('is_solved' in response.data['results'][0])

    def test_get_single_problem(self):
        self.client.get(self.init_url)
        origin = OriginProb.objects.all()[0]
        response = self.client.get(reverse('problems:get_single_problem', kwargs={'origin_id': origin.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['origin']['id'], origin.id)

    def test_create_problem_group(self):
        self.client.get(self.init_url)
        problems = Problem.objects.all().values_list('id', flat=True)
        data = {
            'name': 'test_problem_group',
            'problems': problems,
        }
        response = self.client.post(self.problem_group_api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['problems_count'], 10)

    def test_update_problem_group(self):
        # init (모든 문제 인스턴스화)
        self.client.get(self.init_url)
        # 문제가 없는 그룹 만들기
        response1 = self.client.post(self.problem_group_api_url, { 'name': 'test_problem_group' }, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response1.data['problems_count'], 0)
        # 그룹에 문제 모두(10개) 넣기
        group_id = response1.data['id']
        adding_problems = Problem.objects.all().values_list('id', flat=True)
        data = {
            'adding_problems': adding_problems,
            'removing_problems': [],
        }
        response2 = self.client.post(reverse('problems:single_problem_group_api', kwargs={'group_id': group_id}), data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data['problems_count'], 10)
        # 그룹에서 문제 5개 빼기
        removing_problems = adding_problems[:5]
        data = {
            'adding_problems': [],
            'removing_problems': removing_problems,
        }
        response3 = self.client.post(reverse('problems:single_problem_group_api', kwargs={'group_id': group_id}), data, format='json')
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.data['problems_count'], 5)

    def test_modify_problem_group(self):
        group_id = self.client.post(self.problem_group_api_url, { 'name': 'test_problem_group' }, format='json').data['id']
        data = { 'name': 'new_problem_group' }
        response = self.client.put(reverse('problems:single_problem_group_api', kwargs={'group_id': group_id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])

    def test_delete_problem_group(self):
        group_id = self.client.post(self.problem_group_api_url, { 'name': 'test_problem_group' }, format='json').data['id']
        response = self.client.delete(reverse('problems:single_problem_group_api', kwargs={'group_id': group_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
