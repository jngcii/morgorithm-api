from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SolutionSerializer, CommentSerializer
from .models import Solution, Comment
from problems.models import OriginProb
# from notifications.models import Notification
from users.models import User, Group


def get_solution(solution_id):
    try:
        found_solution = Solution.objects.get(id=solution_id)
        return found_solution
    except Solution.DoesNotExist:
        return None

def get_comment(comment_id):
    try:
        found_comment = Comment.objects.get(id=comment_id)
        return found_comment
    except Comment.DoesNotExist:
        return None


class SolutionAPI(APIView):
    """
    get : get solutions
    post : create solution
    """
    def get(self, request):
        """
        solved (None or true or false)
        user (None or user id)
        problem (None or origin problem id)
        group (None or group id)

        1. 현재 로그인된 유저의 그룹 안에 있는 유저들의 솔루션들만 가져와야 한다.
        2. 가장 많이 걸러질 것 같은 것 순서로 거른다.
        """
        solved = request.GET.get('solved', None)
        user_id = request.GET.get('user', None)
        problem_id = request.GET.get('problem', None)
        group_id = request.GET.get('group', None)

        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            solutions = Solution.objects.filter(creator=user)
        else:
            user = request.user
            groups = user.group.all()
            solutions = Solution.objects.filter(creator__group__in=groups)
        if solved is not None:
            solved = True if solved == 'true' else False
            solutions = solutions.filter(solved=solved)
        if problem_id is not None:
            try:
                problem = OriginProb.objects.get(id=problem_id)
            except OriginProb.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            solutions = solutions.filter(problem=problem)
        if group_id is not None:
            try:
                group = Group.objects.get(id=group_id)
            except Group.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            solutions = solutions.filter(creator__group=group)

        serializer = SolutionSerializer(solutions, many=True)
            
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        request data
        - problem (original problem id)
        - code
        - lang (c, cpp, java, python, javascript 중 하나)
        - solved
        - caption( solved가 True일 때만 받는다.)
        """
        if not request.data.get('problem', None):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            problem = OriginProb.objects.get(id=request.data['problem'])
        except OriginProb.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        serializer = SolutionSerializer(data=request.data)
        if serializer.is_valid():
            solution = serializer.save(creator=user, problem=problem)
            if solution:
                if solution.solved:
                    user_problem = user.problems.get(origin__id=solution.problem.id)
                    user_problem.is_solved = True
                    user_problem.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SolutionDetailAPI(APIView):
    """
    get : get solution detail
    put : modify solution
    delete : delete solution
    """
    def get(self, request, solution_id):
        user = request.user
        found_solution = get_solution(solution_id)
        if not found_solution:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if user.id != found_solution.creator.id:
            found_solution.view += 1
            found_solution.save()
        serializer = SolutionSerializer(found_solution)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, solution_id):
        """
        request data
        - code
        - lang
        - caption
        """
        found_solution = get_solution(solution_id)
        if not found_solution:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SolutionSerializer(found_solution, data=request.data)
        if serializer.is_valid():
            solution = serializer.save()
            if solution:
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, solution_id):
        found_solution = get_solution(solution_id)
        if not found_solution:
            return Response(status=status.HTTP_404_NOT_FOUND)
        found_solution.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class LikeSolution(APIView):

    def get(self, request, solution_id):
        user = request.user
        found_solution = get_solution(solution_id)
        if not found_solution:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if user in found_solution.likes.all():
            found_solution.likes.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            found_solution.likes.add(user)
            return Response(status=status.HTTP_201_CREATED)
        

class CommentAPI(APIView):
    """
    get : get comments of solution
    post : create comment
    """
    def get(self, request, solution_id):
        solution = get_solution(solution_id)
        if not solution:
            return Response(status=status.HTTP_404_NOT_FOUND)
        comments = solution.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request, solution_id):
        """
        ### request data
        - message
        """
        solution = get_solution(solution_id)
        if not solution:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = request.user
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(creator=user, solution=solution)
            if comment:
                # Notification.objects.create(by=user, notification_type='comment', solution=solution, comment=comment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailAPI(APIView):
    """
    put: modify comment
    delete: delete comment
    """
    def put(self, request, comment_id):
        """
        request data
        - message
        """
        found_comment = get_comment(comment_id)
        if not found_comment:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(found_comment, data=request.data)
        if serializer.is_valid():
            comment = serializer.save()
            if comment:
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, _, comment_id):
        found_comment = get_solution(comment_id)
        if not found_comment:
            return Response(status=status.HTTP_404_NOT_FOUND)
        found_comment.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class LikeComment(APIView):

    def get(self, request, comment_id):
        user = request.user
        found_comment = get_comment(comment_id)
        if not found_comment:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if user in found_comment.likes.all():
            found_comment.likes.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            found_comment.likes.add(user)
            return Response(status=status.HTTP_201_CREATED)

# class GetQuestions(APIView):
#     pagination_class = MyPageNumberPagination
#     serializer_class = MiniSolutionSerializer
#     """
#     get all questions only whose own group's user
#     """
#     @property
#     def paginator(self):
#         if not hasattr(self, '_paginator'):
#             if self.pagination_class is None:
#                 self._paginator = None
#             else:
#                 self._paginator = self.pagination_class()
#         else:
#             pass
#         return self._paginator

#     def paginate_queryset(self, queryset):
        
#         if self.paginator is None:
#             return None
#         return self.paginator.paginate_queryset(queryset,
#                    self.request, view=self)

#     def get_paginated_response(self, data):
#         assert self.paginator is not None
#         return self.paginator.get_paginated_response(data)

#     def get(self, request, username):
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
            
#         solutions = user.solutions.filter(solved=False)

#         page = self.paginate_queryset(solutions)
#         if page is not None:
#             serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
#         else:
#             serializer = self.serializer_class(solutions, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)