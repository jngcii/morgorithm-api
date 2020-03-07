from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    CommentSerializer,
    CommentUpdateSerializer,
    SolutionSerializer,
    SolutionUpdateSerializer
)
from .models import Solution, Comment


class SolutionAPI(APIView):
    """
    Solution APIs
    """
    def post(self, request):
        """
        ### request data
        - original problem id
        - code
        - lang (c, cpp, java, python, javascript 중 하나)
        - solved
        - caption( solved가 True일 때만 받는다.)
        """
        user = request.user

        serializer = SolutionSerializer(data=request.data)
        if serializer.is_valid():
            solution = serializer.save(creator=user)
            if solution:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request):
        """
        ### request data
        - solution id
        - code
        - lang
        - solved
        - caption
        """
        if 'id' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            found_solution = Solution.objects.get(id=request.data['id'], creator=request.user)
        except Solution.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = SolutionUpdateSerializer(found_solution, data=request.data)
        if serializer.is_valid():
            solution = serializer.save()
            if solution:
                new_serializer = SolutionSerializer(solution)
                return Response(new_serializer.data, status=status.HTTP_200_OK)
        
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def delete(self, request):
        """
        ### request data
        - solution id
        """
        if 'id' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            solution = Solution.objects.get(id=request.data['id'], creator=request.user)
            solution.delete()
        except Solution.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentAPI(APIView):
    """
    Comment APIs
    """
    def post(self, request):
        """
        ### request data
        - solution id
        - message
        """
        user = request.user
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            comment = serializer.save(creator=user)
            if comment:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        ### request data
        - comment id
        - message
        """
        if 'id' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            found_comment = Comment.objects.get(id=request.data['id'])
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentUpdateSerializer(found_comment, data=request.data)

        if serializer.is_valid():
            comment = serializer.save()
            if comment:
                return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        """
        ### request data
        - comment id
        """
        if 'id' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            found_comment = Comment.objects.get(id=request.data['id'])
            found_comment.delete()
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class ViewCount(APIView):

    def get(self, request, solutionId):

        try:
            solution = Solution.objects.get(id=solutionId)
            solution.view += 1
            solution.save()
            return Response(status=status.HTTP_200_OK)
        except Solution.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LikeSolution(APIView):

    def get(self, request, solutionId):

        user = request.user

        try:
            found_solution = Solution.objects.get(id=solutionId)
        except Solution.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        found_solution.likes.add(user)
        found_solution.save()

        return Response(status=status.HTTP_200_OK)


class UnlikeSolution(APIView):

    def get(self, request, solutionId):

        user = request.user

        try:
            found_solution = Solution.objects.get(id=solutionId)
        except Solution.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        found_solution.likes.remove(user)
        found_solution.save()

        return Response(status=status.HTTP_200_OK)