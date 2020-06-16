from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db.models import Q
from django.utils import timezone
from config.pagination import PaginationHandlerMixin, BasicPagination
from .serializers import OriginProbSerializer, ProbSerializer, ProbGroupSerializer
from .models import OriginProb, Problem, ProblemGroup


class GetProblemList(APIView, PaginationHandlerMixin):
    """
    get problems
    """

    pagination_class = BasicPagination
    serializer_class = ProbSerializer

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


class Fetch(APIView):
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
    
    def get(self, request):
        user = request.user
        last_update = user.last_update

        if last_update:
            origin_probs = OriginProb.objects.filter(created_at__gte=last_update).exclude(id__in=user.problems.values('origin').values_list('id', flat=True))
        else:
            origin_probs = OriginProb.objects.all()

        for origin in origin_probs:
            Problem.objects.create(creator=user, origin=origin)
        
        user.last_update = timezone.localtime()
        user.save()

        all_probs = user.problems.all()
        serializer = ProbSerializer(all_probs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)



class ProblemGroupAPI(APIView):
    """
    create, modify, delete problem group
    """

    def post(self, request):
        """
        request data
        - name (string)
        - problems (problem id list)
        """
        user = request.user
        if user.problem_groups.count() >= 5:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = ProbGroupSerializer(data=request.data)
        if serializer.is_valid():
            group = serializer.save(creator=user)
            if group:
                if 'problems' in request.data:
                    problems = Problem.objects.filter(id__in=request.data['problems'])
                    group.problems.add(*problems)
                new_serializer = ProbGroupSerializer(group)
                return Response(new_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleProblemGroupAPI(APIView):
    """
    post: update problem group
    put: modify problem group
    delete: delete problem group
    """
    def post(self, request, group_id):
        """
        request data
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
        
        adding_problems = Problem.objects.filter(id__in=request.data['adding_problems'])
        group.problems.add(*adding_problems)
        removing_problems = Problem.objects.filter(id__in=request.data['removing_problems'])
        group.problems.remove(*removing_problems)

        serializer = ProbGroupSerializer(group)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, group_id):
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
        try:
            found_group = ProblemGroup.objects.get(id=group_id)
            found_group.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProblemGroup.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# class GetIsIncluding(APIView):
#     """
#     get groups not include problem
#     """
#     def get(self, request, group_id, prob_id):
#         """
#         param : problem group id, problem id
#         """
#         user = request.user
#         try:
#             group = ProblemGroup.objects.get(id=group_id)
#         except ProblemGroup.DoesNotExist:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         if group.problems.filter(id=prob_id).exists():
#             return Response({ 'is_exist': True }, status=status.HTTP_200_OK)
#         else:
#             return Response({ 'is_exist': False }, status=status.HTTP_200_OK)
