from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from .models import OriginProb, Problem, ProblemGroup
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


class ProbGroupsTest(APITestCase):

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

    def test_upload_problems_to_group(self):
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
        response = self.client.post(reverse('upload-problems-to-group'), adding_data, format='json')
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
        response = self.client.post(reverse('upload-problems-to-group'), removing_data, format='json')
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
        response = self.client.post(reverse('upload-problems-to-group'), adding_data, format='json')
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
        response = self.client.post(reverse('upload-problems-to-group'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['problems']), 0)
    
    def test_upload_problems_to_group_without_group_id(self):
        """
        test uplo9ad problems to group without group id
        """
        self.test_add_group()
        data = {
            'adding_problems': [],
            'removing_problems': [],
        }
        response = self.client.post(reverse('upload-problems-to-group'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_upload_problems_to_group_by_wrong_type(self):
        """
        test uplo9ad problems to group by worng type
        """
        self.test_add_group()
        data = {
            'adding_problems': 1,
            'removing_problems': 4,
        }
        response = self.client.post(reverse('upload-problems-to-group'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)