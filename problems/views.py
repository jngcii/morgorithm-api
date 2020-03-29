from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .serializers import (
    OriginProbSerializer,
    ProbSerializer,
    CopyProbSerializer,
    ProbGroupSerializer,
)
from .models import OriginProb, Problem, ProblemGroup

class AddOriginProb(APIView):
    """
    Add original problem by administrator
    """
    
    def post(self, request):
        user = request.user

        if not user.is_admin:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = OriginProbSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CopyAndGetProbs(APIView):
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


class ProblemGroupAPI(APIView):
    """
    add, modify, delete problem group
    """

    def post(self, request):
        """
        request data
        - name (group name)
        """
        user = request.user
        if user.problem_groups.count() >= 5:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = ProbGroupSerializer(data=request.data)
        if serializer.is_valid():
            group = serializer.save(creator=user)
            if group:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        request data
        - id (prob group id)
        - name (new group name)
        """
        if 'id' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            found_group = ProblemGroup.objects.get(id=request.data['id'])
        except ProblemGroup.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = ProbGroupSerializer(found_group, data=request.data)
        if serializer.is_valid():
            group = serializer.save()
            if group:
                return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        request data
        - id (prob group id)
        """
        if 'id' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            found_group = ProblemGroup.objects.get(id=request.data['id'])
            found_group.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProblemGroup.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateProblemsToGroup(APIView):
    """
    add problems in problem group
    """
    def post(self, request):
        """
        request data
        - id (problem group id)
        - adding_problems (list of problems id)
        - removing_problems (list of problems id)
        """
        if 'id' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if 'adding_problems' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if 'removing_problems' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if type(request.data['adding_problems']) is not list or type(request.data['removing_problems']) is not list:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            group = ProblemGroup.objects.get(id=request.data['id'])
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


class GetProblems(APIView):
    """
    get problems
    """
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
        problems = user.problems.all()
        if 'group' in request.data:
            problems = problems.filter(group__id__in=request.data['group'])
        if 'category' in request.data:
            problems = problems.filter(origin__category__in=request.data['category'])
        if 'level' in request.data:
            problems = problems.filter(origin__level__in=request.data['level'])
        if 'solved' in request.data:
            problems = problems.filter(solved=request.data['solved'])
        if 'keyword' in request.data:
            problems = problems.filter(
                Q(origin__number=int(request.data['keyword']))
                |Q(origin__number=request.data['keyword'])
                |Q(origin__title__icontains=request.data['keyword'])
                |Q(origin_remark__icontains=request.data['keyword'])
            )
            
        serializer = ProbSerializer(problems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)