from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from problems.models import OriginProb
from users.models import User, Group
# from rest_framework import status
# from pprint import pprint

class SolutionTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.solutions_api_url = reverse('solutions:solution_api')

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
            group.members.add(*groups[i-1], self.test_user)

        for i in range(1, 11):
            data = {
                'url': 'https://www.acmicpc.net/problem/{}'.format(i),
                'number': i,
                'category': 'BOJ',
                'title': 'test {}'.format(i)
            }
            OriginProb.objects.create(**data)
    
    def test_get_group_members(self):
        self.client.get(self.solutions_api_url)