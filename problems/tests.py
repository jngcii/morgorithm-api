from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from .models import OriginProb, Problem, ProblemGroup
from users.models import User
from rest_framework import status
# from pprint import pprint

class ProbsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.get_problem_list_url = reverse('problems:get_problem_list')
        self.init_url = reverse('problems:init')
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
    

    def test_init(self):
        response = self.client.get(self.init_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Problem.objects.count(), 10)

    def test_get_problem_list(self):
        self.client.get(self.init_url)
        response = self.client.post(self.get_problem_list_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertTrue('origin' in response.data['results'][0])
        self.assertTrue('is_solved' in response.data['results'][0])

    def test_get_single_problem(self):
        self.client.get(self.init_url)
        origin = OriginProb.objects.all()[0]
        response = self.client.get(reverse('problems:get_single_problem', kwargs={'origin_id': origin.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['origin']['id'], origin.id)



class ProbGroupsTest(APITestCase):

    # path('group/', views.ProbGroupsAPI.as_view(), name='problem-group-api'),# 모든 그룹 가져오기, 그룹 만들기
    # path('group/<int:group_id>/', views.ProbGroupAPI.as_view(), name='problem-group-api'),# 그룹 업데이트(문제 넣고 빼기), 그룹 수정(그룹명), 그룹 삭제
    # path('group/<int:group_id>/<int:prob_id>/', views.GetIsIncluding.as_view(), name='is_including_problem'),

    def setUp(self):
        self.client = APIClient()

        self.sign_up_url = reverse('sign-up')
        self.sign_in_url = reverse('sign-in')
        self.add_origin_prob_url = reverse('add-origin-prob')
        self.copy_and_get_props_url = reverse('copy-and-get-probs')
        self.solution_api_url = reverse('solution-api')
        self.comment_api_url = reverse('comment-api')

        self.super_credential = {
            'username': 'root',
            'email': 'root@hmc.com',
            'password': 'asdf1488'
        }
        self.super_user_data = {
            'username': 'root',
            'password': 'asdf1488'
        }

        self.credential_1 = {
            'username': 'testuser1',
            'email': 'test1@example.com',
            'password': 'testpassword'
        }
        self.user_data_1 = {
            'username': 'testuser1',
            'password': 'testpassword'
        }

        self.credential_2 = {
            'username': 'testuser2',
            'email': 'test2@example.com',
            'password': 'testpassword'
        }
        self.user_data_2 = {
            'username': 'testuser2',
            'password': 'testpassword'
        }

        User.objects.create_superuser(**self.super_credential)
        User.objects.create_user(**self.credential_1)
        User.objects.create_user(**self.credential_2)

        self.test_superuser = self.client.post(self.sign_in_url, self.super_user_data, format='json')
        self.test_user_1 = self.client.post(self.sign_in_url, self.user_data_1, format='json')
        self.test_user_2 = self.client.post(self.sign_in_url, self.user_data_2, format='json')

        self.origin_prob_data_1 = {
            'url': 'https://www.acmicpc.net/problem/1339',
            'number': 1339,
            'category': 'BOJ',
            'title': '[S/W 문제해결 기본] 8일차 - 암호문3'
        }
        self.origin_prob_data_2 = {
            'url': 'https://www.acmicpc.net/problem/1340',
            'number': 1340,
            'category': 'BOJ',
            'title': '[S/W 문제해결 기본] 8일차 - 암호문4'
        }
        self.origin_prob_data_3 = {
            'url': 'https://www.acmicpc.net/problem/1341',
            'number': 1341,
            'category': 'BOJ',
            'title': '[S/W 문제해결 기본] 8일차 - 암호문5'
        }
        self.origin_prob_data_4 = {
            'url': 'https://www.acmicpc.net/problem/1342',
            'number': 1342,
            'category': 'BOJ',
            'title': '[S/W 문제해결 기본] 8일차 - 암호문6'
        }
        self.origin_prob_data_5 = {
            'url': 'https://www.acmicpc.net/problem/1343',
            'number': 1343,
            'category': 'BOJ',
            'title': '[S/W 문제해결 기본] 8일차 - 암호문7'
        }
        self.origin_prob_data_6 = {
            'url': 'https://www.acmicpc.net/problem/1344',
            'number': 1344,
            'category': 'BOJ',
            'title': '[S/W 문제해결 기본] 8일차 - 암호문8'
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.test_superuser.data['token']))
        self.client.post(self.add_origin_prob_url, self.origin_prob_data_1, format='json')
        self.client.post(self.add_origin_prob_url, self.origin_prob_data_2, format='json')
        self.client.post(self.add_origin_prob_url, self.origin_prob_data_3, format='json')
        self.client.post(self.add_origin_prob_url, self.origin_prob_data_4, format='json')
        self.client.post(self.add_origin_prob_url, self.origin_prob_data_5, format='json')
        self.client.post(self.add_origin_prob_url, self.origin_prob_data_6, format='json')

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.test_user_1.data['token']))
        self.copy_res_1 = self.client.get(self.copy_and_get_props_url)
        self.assertEqual(self.copy_res_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(self.copy_res_1.data), 6)

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.test_user_2.data['token']))
        self.copy_res_2 = self.client.get(self.copy_and_get_props_url)
        self.assertEqual(self.copy_res_2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(self.copy_res_2.data), 6)

    def test_add_group(self):
        data = {
            'name': 'test-prob-group',
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.test_user_1.data['token']))
        response = self.client.post(reverse('problem-group-api'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])

    def test_add_too_many_group(self):
        data = {
            'name': 'test-prob-group',
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.test_user_1.data['token']))
        self.client.post(reverse('problem-group-api'), data, format='json')
        self.client.post(reverse('problem-group-api'), data, format='json')
        self.client.post(reverse('problem-group-api'), data, format='json')
        self.client.post(reverse('problem-group-api'), data, format='json')
        self.client.post(reverse('problem-group-api'), data, format='json')
        response = self.client.post(reverse('problem-group-api'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ProblemGroup.objects.count(), 5)

    def test_add_group_with_empty_name(self):
        data = {
            'name': '',
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.test_user_1.data['token']))
        response = self.client.post(reverse('problem-group-api'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_modify_group(self):
        self.test_add_group()
        data = {
            'id': ProblemGroup.objects.latest('id').id,
            'name': 'new test problem group',
        }
        response = self.client.put(reverse('problem-group-api'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])

    def test_delete_group(self):
        self.test_add_group()
        data = {
            'id': ProblemGroup.objects.latest('id').id,
        }
        response = self.client.delete(reverse('problem-group-api'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_problems_to_group(self):
        """
        test adding and removing problems to group
        """
        self.test_add_group()
        adding_data = {
            'id': ProblemGroup.objects.latest('id').id,
            'adding_problems': [
                self.copy_res_1.data[0]['id'],
                self.copy_res_1.data[1]['id'],
                self.copy_res_1.data[2]['id'],
                self.copy_res_1.data[3]['id'],
                self.copy_res_1.data[4]['id'],
            ],
            'removing_problems': [],
        }
        response = self.client.post(reverse('update-problems-to-group'), adding_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['problems']), 5)

        removing_data = {
            'id': ProblemGroup.objects.latest('id').id,
            'adding_problems': [],
            'removing_problems': [
                self.copy_res_1.data[0]['id'],
                self.copy_res_1.data[1]['id'],
            ],
        }
        response = self.client.post(reverse('update-problems-to-group'), removing_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['problems']), 3)

    def test_add_same_problems_to_group(self):
        """
        test adding same problems to groups
        """
        self.test_add_group()
        adding_data = {
            'id': ProblemGroup.objects.latest('id').id,
            'adding_problems': [
                self.copy_res_1.data[0]['id'],
                self.copy_res_1.data[0]['id'],
                self.copy_res_1.data[0]['id'],
                self.copy_res_1.data[0]['id'],
                self.copy_res_1.data[0]['id'],
            ],
            'removing_problems': [],
        }
        response = self.client.post(reverse('update-problems-to-group'), adding_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['problems']), 1)

    def test_remove_non_existing_problems_to_group(self):
        """
        test removing non-existing problems to groups
        """
        self.test_add_group()
        data = {
            'id': ProblemGroup.objects.latest('id').id,
            'adding_problems': [],
            'removing_problems': [
                self.copy_res_1.data[0]['id'],
                self.copy_res_1.data[1]['id'],
                self.copy_res_1.data[2]['id'],
                self.copy_res_1.data[3]['id'],
                self.copy_res_1.data[0]['id'],
            ],
        }
        response = self.client.post(reverse('update-problems-to-group'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['problems']), 0)
    
    def test_update_problems_to_group_without_group_id(self):
        """
        test uplo9ad problems to group without group id
        """
        self.test_add_group()
        data = {
            'adding_problems': [],
            'removing_problems': [],
        }
        response = self.client.post(reverse('update-problems-to-group'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_problems_to_group_by_wrong_type(self):
        """
        test uplo9ad problems to group by worng type
        """
        self.test_add_group()
        data = {
            'adding_problems': 1,
            'removing_problems': 4,
        }
        response = self.client.post(reverse('update-problems-to-group'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)