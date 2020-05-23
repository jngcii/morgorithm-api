from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .serializers import (
    OriginProbSerializer,
    ProbSerializer,
    CopyProbSerializer,
    ProbGroupSerializer,
)
from .models import OriginProb, Problem, ProblemGroup



class MyPageNumberPagination(PageNumberPagination):
    page_size = 10



class GetProblemList(APIView):
    pagination_class = MyPageNumberPagination
    serializer_class = ProbSerializer
    """
    get problems
    """

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):
        
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset,
                   self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def post(self, request):
        """
        request data
        - group : array of probGroupId. if empty, all problems
        - category : array of category. if empty, all problems
        - level : array of level. if empty, all levels
        - solved : 없거나 true or false
        - keyword : string
        """
        user = request.user
        problems = Problem.objects.filter(creator=user)

        if 'group' in request.data and len(request.data['group']):
            problems = problems.filter(group__id__in=request.data['group'])
        if 'category' in request.data and len(request.data['category']):
            problems = problems.filter(origin__category__in=request.data['category'])
        if 'level' in request.data and len(request.data['level']):
            problems = problems.filter(Q(origin__level__in=request.data['level'])|Q(origin__level=None))
        if 'solved' in request.data and len(request.data['solved']):
            problems = problems.filter(is_solved__in=request.data['solved'])
        if 'keyword' in request.data:
            problems = problems.filter(
                Q(origin__number=request.data['keyword'] if request.data['keyword'].isdigit() else 0)
                |Q(origin__title__icontains=request.data['keyword'])
                |Q(origin__remark__icontains=request.data['keyword'])
            )
            
        page = self.paginate_queryset(problems)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(problems, many=True)   
        # serializer = ProbSerializer(problems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetSingleProblem(APIView):
    """
    get single problem py origin problem id
    """
    def get(self, request, origin_id):
        """
        param : origin_id (original problem id)
        """
        user = request.user
        try:
            problem = user.problems.get(origin__id=origin_id)
        except Problem.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = ProbSerializer(problem)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProbGroupsAPI(APIView):
    """
    create, modify, delete problem group
    """

    def post(self, request):
        """
        request data
        - name (groupName)
        - probIds
        """
        user = request.user
        if user.problem_groups.count() >= 5:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = ProbGroupSerializer(data=request.data)
        if serializer.is_valid():
            group = serializer.save(creator=user)
            if group:
                if 'probIds' in request.data:
                    for problem_id in request.data['probIds']:
                        try:
                            prob = Problem.objects.get(id=problem_id)
                            group.problems.add(prob)
                        except Problem.DoesNotExist:
                            continue
                    group.save()
                    new_serializer = ProbGroupSerializer(group)
                return Response(new_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProbGroupAPI(APIView):
    """
    post: update problem group
    put: modify problem group
    delete: delete problem group
    """
    def post(self, request, group_id):
        """
        request data
        - id (problem group id)
        - adding_problems (list of problems id)
        - removing_problems (list of problems id)
        """
        if 'adding_problems' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if 'removing_problems' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if type(request.data['adding_problems']) is not list or type(request.data['removing_problems']) is not list:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            group = ProblemGroup.objects.get(id=group_id)
        except ProblemGroup.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        for idx in request.data['adding_problems']:
            try:
                problem = Problem.objects.get(id=idx)
                group.problems.add(problem)
            except Problem.DoesNotExist:
                continue
        
        for idx in request.data['removing_problems']:
            try:
                problem = Problem.objects.get(id=idx)
                group.problems.remove(problem)
            except Problem.DoesNotExist:
                continue

        group.save()
        serializer = ProbGroupSerializer(group)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, group_id):
        """
        request data
        - id (prob group id)
        - name (new group name)
        """
        try:
            found_group = ProblemGroup.objects.get(id=group_id)
        except ProblemGroup.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = ProbGroupSerializer(found_group, data=request.data)
        if serializer.is_valid():
            group = serializer.save()
            if group:
                return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, group_id):
        """
        request data
        - id (prob group id)
        """
        try:
            found_group = ProblemGroup.objects.get(id=group_id)
            found_group.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProblemGroup.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GetIsIncluding(APIView):
    """
    get groups not include problem
    """
    def get(self, request, group_id, prob_id):
        """
        param : problem group id, problem id
        """
        user = request.user
        try:
            group = ProblemGroup.objects.get(id=group_id)
        except ProblemGroup.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if group.problems.filter(id=prob_id).exists():
            return Response({ 'is_exist': True }, status=status.HTTP_200_OK)
        else:
            return Response({ 'is_exist': False }, status=status.HTTP_200_OK)


class FetchProb(APIView):
    permission_classes = [AllowAny]
    """
    Add original problem by administrator
    """
    
    def post(self, request):
        # user = request.user

        # if not user.is_admin:
        #     return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = OriginProbSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Init(APIView):
    """
    copy all original problems to current user's problem
    """

    def get_user_probs(self, user):
        try:
            probs = Problem.objects.filter(creator=user)
            return probs
        except Problem.DoesNotExist:
            return None
    
    def get(self, request):
        user = request.user
        try:
            origin_probs = OriginProb.objects.all()
        except OriginProb.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        probs = self.get_user_probs(user)
        if probs is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        for origin in origin_probs:
            flag = False
            for prob in probs:
                if prob.origin == origin:
                    flag = True
            if flag:
                continue
            
            copy_serializer = CopyProbSerializer(data={'origin': origin.id})
            if copy_serializer.is_valid():
                copy_serializer.save(creator=user)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        
        all_probs = self.get_user_probs(user)
        if all_probs is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = ProbSerializer(all_probs, many=True)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
