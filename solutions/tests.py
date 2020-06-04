from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Solution, Comment
from users.models import User, Group
from problems.models import OriginProb
# from pprint import pprint

class SolutionTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.credential = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        self.test_user = User.objects.create_user(**self.credential)
        self.client.force_authenticate(user=self.test_user)

        for i in range(1, 11):
            data = {
                'username': 'user{}'.format(i),
                'email': 'user{}@example.com'.format(i),
                'password': 'testpassword'
            }
            User.objects.create_user(**data)

        groups = [User.objects.all()[1:4], User.objects.all()[4:7], User.objects.all()[7:10]]

        for i in range(1, 4):
            group = Group.objects.create(name='group{}'.format(i))
            group.members.add(*groups[i-1])
            if i%2:
                group.members.add(self.test_user)

        for i in range(1, 11):
            data = {
                'url': 'https://www.acmicpc.net/problem/{}'.format(i),
                'number': i,
                'category': 'BOJ',
                'title': 'test {}'.format(i)
            }
            OriginProb.objects.create(**data)
        
        self.test_problem = OriginProb.objects.latest('id')

        for i in range(1, 11):
            data = {
                'creator': self.test_user,
                'problem': self.test_problem,
                'code': f'def func{i}(): return {i}',
                'lang': 'python',
                'solved': i % 2,
            }
            Solution.objects.create(**data)
        
        self.test_solution = Solution.objects.order_by('created_at')[0]

        for i in range(1, 11):
            data = {
                'creator': self.test_user,
                'solution': self.test_solution,
                'message': f'comment {i}',
            }
            Comment.objects.create(**data)

        self.test_comment = Comment.objects.latest('id')

        self.init_url = reverse('problems:init')
        self.solution_api_url = reverse('solutions:solution_api')
        self.solution_detail_api_url = reverse('solutions:solution_detail_api', kwargs={'solution_id': self.test_solution.id})
        self.comment_api_url = reverse('solutions:comment_api', kwargs={'solution_id': self.test_solution.id})
    

    def test_get_solutions_in(self):
        user = User.objects.filter(group__name='group1')[0]
        self.client.force_authenticate(user=user)
        response = self.client.get(self.solution_api_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_get_solved_solutions_in(self):
        user = User.objects.filter(group__name='group1')[0]
        self.client.force_authenticate(user=user)
        response = self.client.get(self.solution_api_url, {'solved': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['solved'], True)
        self.assertEqual(len(response.data), 5)

    def test_get_user_solutions(self):
        user = User.objects.filter(group__name='group1')[0]
        self.client.force_authenticate(user=user)
        response = self.client.get(self.solution_api_url, {'user': self.test_user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_get_solutions_out(self):
        user = User.objects.filter(group__name='group2')[0]
        self.client.force_authenticate(user=user)
        response = self.client.get(self.solution_api_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_post_solved_solution(self):
        self.client.get(self.init_url)
        data = {
            'problem': self.test_problem.id,
            'code': 'def go(a, b): return a + b',
            'lang': 'python',
            'solved': True,
        }
        response = self.client.post(self.solution_api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['problem']['id'], data['problem'])
        self.assertEqual(response.data['solved'], data['solved'])

    def test_get_solution_detail(self):
        response = self.client.get(self.solution_detail_api_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], self.test_solution.code)
        self.assertEqual(response.data['creator']['username'], self.test_user.username)

    def test_put_solution_detail(self):
        data = {
            'code': 'def put(): return 1',
        }
        response = self.client.put(self.solution_detail_api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], data['code'])

    def test_delete_solution_detail(self):
        response = self.client.delete(self.solution_detail_api_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Solution.objects.count(), 9)

    def test_get_comments(self):
        response = self.client.get(self.comment_api_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.count(), 10)

    def test_post_comment(self):
        data = {
            'message': 'changed!',
        }
        response = self.client.post(self.comment_api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], data['message'])
        self.assertEqual(response.data['solution'], self.test_solution.id)
        self.assertTrue('is_liked' in response.data)