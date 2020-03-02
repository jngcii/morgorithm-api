from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OriginProbSerializer
# from .models import OriginProb

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
