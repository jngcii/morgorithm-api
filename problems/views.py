from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OriginProbSerializer, ProbSerializer, CopyProbSerializer
from .models import OriginProb, Problem

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