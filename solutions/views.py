from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SolutionSerializer
from .models import Solution


class SolutionAPI(APIView):
    """
    Add solution
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

    
    def delete(self, request):
        """
        ### request data
        - solution id
        """
        try:
            solution = Solution.objects.get(id=request.data['solutionId'])
            solution.delete()
        except Solution.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)

