from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from .models import Solution, Comment
from problems.models import Problem
from users.models import User
from rest_framework import status
# from pprint import pprint

class SolutionTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.sign_up_url = reverse('sign-up')
        self.sign_in_url = reverse('sign-in')
        self.add_origin_prob_url = reverse('add-origin-prob')
        self.copy_and_get_props_url = reverse('copy-and-get-probs')
        self.solution_api_url = reverse('solution-api')
        self.comment_api_url = reverse('comment-api')
        self.sub_comment_api_url = reverse('sub-comment-api')

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

        self.assertEqual(Problem.objects.latest('id').is_solved, False)
        response = self.client.post(self.solution_api_url, data, format='json')
        # pprint(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Solution.objects.count(), 1)
        self.assertEqual(Problem.objects.latest('id').is_solved, True)
        self.assertEqual(response.data['view'], 0)
        self.assertFalse(response.data['caption'])
        self.assertEqual(len(response.data['comments']), 0)

    def test_add_unsolved_solution(self):
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

        response = self.client.post(self.solution_api_url, data, format='json')
        # pprint(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Solution.objects.count(), 1)
        self.assertEqual(response.data['view'], 0)
        self.assertEqual(response.data['caption'], data['caption'])

    def test_delete_solution(self):
        """
        test deleting solution
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

        add_res = self.client.post(self.solution_api_url, data, format='json')
        # pprint(add_res.data)
        self.assertEqual(add_res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Solution.objects.count(), 1)

        data2 = {
            'id': add_res.data['id']
        }

        delete_res = self.client.delete(self.solution_api_url, data2, format='json')
        self.assertEqual(delete_res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Solution.objects.count(), 0)

    def test_delete_solution_with_wrong_solution_id(self):
        """
        test deleting solution
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

        add_res = self.client.post(self.solution_api_url, data, format='json')
        # pprint(add_res.data)
        self.assertEqual(add_res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Solution.objects.count(), 1)

        data2 = {
            'id': 1000
        }

        delete_res = self.client.delete(self.solution_api_url, data2, format='json')
        self.assertEqual(delete_res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Solution.objects.count(), 1)

    def test_update_solution(self):
        """
        test deleting solution
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

        add_res = self.client.post(self.solution_api_url, data, format='json')
        self.assertEqual(add_res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Solution.objects.count(), 1)

        data2 = {
            'id': add_res.data['id'],
            'code': """def multiple(a, b):
            return a * b
            """,
            'caption': None,
            'lang': 'python',
            'solved': True
        }

        update_res = self.client.put(self.solution_api_url, data2, format='json')
        self.assertEqual(update_res.status_code, status.HTTP_200_OK)
        self.assertEqual(Solution.objects.count(), 1)
        self.assertEqual(update_res.data['solved'], True)

    def test_update_solution_with_no_info(self):
        """
        test deleting solution
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

        add_res = self.client.post(self.solution_api_url, data, format='json')
        self.assertEqual(add_res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Solution.objects.count(), 1)

        data2 = {
            'id': add_res.data['id'],
        }

        update_res = self.client.put(self.solution_api_url, data2, format='json')
        self.assertEqual(update_res.status_code, status.HTTP_200_OK)
        self.assertEqual(Solution.objects.count(), 1)
        self.assertEqual(update_res.data['solved'], False)

    def test_update_solution_with_no_solution_id(self):
        """
        test deleting solution
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

        add_res = self.client.post(self.solution_api_url, data, format='json')
        self.assertEqual(add_res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Solution.objects.count(), 1)

        data2 = {
        }

        update_res = self.client.put(self.solution_api_url, data2, format='json')
        self.assertEqual(update_res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_count(self):
        """
        test view count
        """
        data = {
            'problem': self.copy_res.data[0]['origin']['id'],
            'code': """def add(a, b):
            return a + b
            """,
            'lang': 'python',
            'solved': True
        }

        response = self.client.post(self.solution_api_url, data, format='json')
        # pprint(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Solution.objects.count(), 1)
        self.assertEqual(response.data['view'], 0)
        
        sol_res = self.client.get(reverse('view-solution', kwargs={'solutionId': response.data['id']}))
        self.assertEqual(sol_res.status_code, status.HTTP_200_OK)
        self.assertEqual(Solution.objects.get(id=response.data['id']).view, 1)

    def test_view_count_with_invalid_id(self):
        """
        test view count
        """
        data = {
            'problem': self.copy_res.data[0]['origin']['id'],
            'code': """def add(a, b):
            return a + b
            """,
            'lang': 'python',
            'solved': True
        }

        response = self.client.post(self.solution_api_url, data, format='json')
        # pprint(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Solution.objects.count(), 1)
        self.assertEqual(response.data['view'], 0)
        
        sol_res = self.client.get(reverse('view-solution', kwargs={'solutionId': 1111}))
        self.assertEqual(sol_res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Solution.objects.get(id=response.data['id']).view, 0)

    def test_like_unlike_solution(self):
        """
        test like solution and unlike solution
        """
        self.test_add_solved_solution()
        solution = Solution.objects.latest('id')
        like_res = self.client.get(reverse('like-solution', kwargs={'solutionId': solution.id}))
        self.assertEqual(like_res.status_code, status.HTTP_200_OK)
        self.assertEqual(Solution.objects.get(id=solution.id).like_count, 1)

        unlike_res = self.client.get(reverse('unlike-solution', kwargs={'solutionId': solution.id}))
        self.assertEqual(unlike_res.status_code, status.HTTP_200_OK)
        self.assertEqual(Solution.objects.get(id=solution.id).like_count, 0)
    
    def test_double_like_unlike_solution(self):
        """
        test like solution and unlike solution
        """
        self.test_add_solved_solution()
        solution = Solution.objects.latest('id')
        self.client.get(reverse('like-solution', kwargs={'solutionId': solution.id}))
        like_res = self.client.get(reverse('like-solution', kwargs={'solutionId': solution.id}))
        self.assertEqual(like_res.status_code, status.HTTP_200_OK)
        self.assertEqual(Solution.objects.get(id=solution.id).like_count, 1)

        self.client.get(reverse('unlike-solution', kwargs={'solutionId': solution.id}))
        unlike_res = self.client.get(reverse('unlike-solution', kwargs={'solutionId': solution.id}))
        self.assertEqual(unlike_res.status_code, status.HTTP_200_OK)
        self.assertEqual(Solution.objects.get(id=solution.id).like_count, 0)

    def test_add_comment(self):
        """
        test adding comment
        """
        self.test_add_solved_solution()
        solution = Solution.objects.latest('id')
        data = {
            'solution': solution.id,
            'message': 'yay',
        }
        response = self.client.post(self.comment_api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], data['message'])
        self.assertEqual(Comment.objects.all().count(), 1)

    def test_add_comment_without_message(self):
        """
        test adding comment without message
        """
        self.test_add_solved_solution()
        solution = Solution.objects.latest('id')
        data = {
            'solution': solution.id,
            'message': '',
        }
        response = self.client.post(self.comment_api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.all().count(), 0)

    def test_modify_comment(self):
        """
        test modifying comment
        """
        self.test_add_comment()
        comment = Comment.objects.latest('id')
        data = {
            'id': comment.id,
            'message': 'modified!',
        }
        response = self.client.put(self.comment_api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], data['message'])
        self.assertEqual(Comment.objects.all().count(), 1)

    def test_modify_comment_without_comment_id(self):
        """
        test modifying comment without comment id
        """
        self.test_add_comment()
        data = {
            'message': 'modified!',
        }
        response = self.client.put(self.comment_api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.all().count(), 1)

    def test_delete_comment(self):
        """
        test deleting comment
        """
        self.test_add_comment()
        comment = Comment.objects.latest('id')
        data = {
            'id': comment.id,
        }
        response = self.client.delete(self.comment_api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.all().count(), 0)

    def test_delete_comment_without_comment_id(self):
        """
        test deleting comment
        """
        self.test_add_comment()
        response = self.client.delete(self.comment_api_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.all().count(), 1)

    def test_sub_add_comment(self):
        """
        test adding comment
        """
        self.test_add_comment()
        comment = Comment.objects.latest('id')
        data = {
            'comment': comment.id,
            'message': 'yayay',
        }
        response = self.client.post(self.sub_comment_api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], data['message'])
        self.assertEqual(Comment.objects.all().count(), 1)

    def test_get_solution(self):
        """
        test getting solution
        """
        self.test_add_comment()
        solution = Solution.objects.latest('id')
        response = self.client.get(reverse('get-solution', kwargs={'solutionId': solution.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['comments']), 1)
        self.assertEqual(response.data['comment_count'], 1)
        self.assertEqual(len(response.data['likes']), 0)
        self.assertEqual(response.data['like_count'], 0)



class GetSolutionTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.sign_up_url = reverse('sign-up')
        self.sign_in_url = reverse('sign-in')
        self.create_group_url = reverse('create-group')
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

        self.credential_3 = {
            'username': 'testuser3',
            'email': 'test3@example.com',
            'password': 'testpassword'
        }
        self.user_data_3 = {
            'username': 'testuser3',
            'password': 'testpassword'
        }

        self.credential_4 = {
            'username': 'testuser4',
            'email': 'test4@example.com',
            'password': 'testpassword'
        }
        self.user_data_4 = {
            'username': 'testuser4',
            'password': 'testpassword'
        }

        User.objects.create_superuser(**self.super_credential)
        User.objects.create_user(**self.credential_1)
        User.objects.create_user(**self.credential_2)
        User.objects.create_user(**self.credential_3)
        User.objects.create_user(**self.credential_4)

        self.test_superuser = self.client.post(self.sign_in_url, self.super_user_data, format='json')
        self.test_user_1 = self.client.post(self.sign_in_url, self.user_data_1, format='json')
        self.test_user_2 = self.client.post(self.sign_in_url, self.user_data_2, format='json')
        self.test_user_3 = self.client.post(self.sign_in_url, self.user_data_3, format='json')
        self.test_user_4 = self.client.post(self.sign_in_url, self.user_data_4, format='json')

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.test_user_1.data['token']))
        self.group_res = self.client.post(self.create_group_url, {'name': 'testgroup'}, format='json')
        self.assertEqual(self.group_res.status_code, status.HTTP_201_CREATED)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.test_user_2.data['token']))
        self.enter_res_2 = self.client.post(reverse('enter-group', kwargs={'groupId':self.group_res.data['id']}))
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.test_user_3.data['token']))
        self.enter_res_3 = self.client.post(reverse('enter-group', kwargs={'groupId':self.group_res.data['id']}))
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.test_user_4.data['token']))
        self.enter_res_4 = self.client.post(reverse('enter-group', kwargs={'groupId':self.group_res.data['id']}))

        self.origin_prob_data = {
            'url': 'https://www.acmicpc.net/problem/1339',
            'number': 1339,
            'category': 'BOJ',
            'title': '[S/W 문제해결 기본] 8일차 - 암호문3'
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.test_superuser.data['token']))
        self.client.post(self.add_origin_prob_url, self.origin_prob_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.test_user_1.data['token']))
        self.copy_res = self.client.get(self.copy_and_get_props_url)
        self.assertEqual(self.copy_res.status_code, status.HTTP_201_CREATED)

        self.solved_data = {
            'problem': self.copy_res.data[0]['origin']['id'],
            'code': """def add(a, b):
            return a + b
            """,
            'lang': 'python',
            'solved': True
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.test_user_2.data['token']))
        response = self.client.post(self.solution_api_url, self.solved_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.unsolved_data = {
            'problem': self.copy_res.data[0]['origin']['id'],
            'code': """
            print('oh no')
            """,
            'caption': '뭐가 틀린지 모르겠어요.',
            'lang': 'python',
            'solved': False
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.test_user_3.data['token']))
        response = self.client.post(self.solution_api_url, self.unsolved_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_solutions(self):
        """
        test get all solutions
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.test_user_1.data['token']))
        response = self.client.get(reverse('get-all-solutions', kwargs={'originId': self.copy_res.data[0]['id']}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_all_questions(self):
        """
        test get all questions
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.test_user_1.data['token']))
        response = self.client.get(reverse('get-all-questions'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['creator']['username'], self.user_data_3['username'])
        self.assertEqual(response.data[0]['solved'], False)
        self.assertEqual(len(response.data), 1)

    def test_search_questions_by_title(self):
        """
        test search questions by title
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.test_user_1.data['token']))
        response = self.client.get(reverse('search-questions', kwargs={'txt': '암호문'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['creator']['username'], self.user_data_3['username'])
        self.assertEqual(response.data[0]['solved'], False)

    def test_search_questions_by_number(self):
        """
        test search questions by title
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.test_user_1.data['token']))
        response = self.client.get(reverse('search-questions', kwargs={'txt': self.origin_prob_data['number']}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['creator']['username'], self.user_data_3['username'])
        self.assertEqual(response.data[0]['solved'], False)

    def test_search_questions_nonexisting_data(self):
        """
        test search questions by title
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.test_user_1.data['token']))
        response = self.client.get(reverse('search-questions', kwargs={'txt': 2}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

