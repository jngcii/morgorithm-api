from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SolutionSerializer
# from .models import Solution


class AddSolution(APIView):
    """
    Add solution
    """
    def post(self, request):
        user = request.user

        serializer = SolutionSerializer(data=request.data)
        if serializer.is_valid():
            solution = serializer.save(creator=user)
            if solution:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)