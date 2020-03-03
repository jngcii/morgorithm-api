from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LogInSerializer, GroupSerializer
from .models import User, Group
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny


class SignUp(APIView):
    """ 
    Creates the user. 
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignIn(APIView):
    """
    Log user in
    """
    permission_classes = [AllowAny]

    def get_user(self, request):
        username = request.data['username']
        password = request.data['password']
        try:
            user = User.objects.get(username=username)
            if user and user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def post(self, request):
        serializer = LogInSerializer(data=request.data)

        if serializer.is_valid():
            user = self.get_user(request)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateGroup(APIView):
    """ 
    Creates the group. 
    """
    def post(self, request):
        user = request.user
        if user.group.count()>=5:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            group = serializer.save()
            if group:
                group.members.add(user)
                group.save()
                new_serializer = GroupSerializer(group)
                return Response(new_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnterGroup(APIView):
    """
    Enter the group
    """
    def get(self, request, groupId):
        user = request.user

        try:
            group = Group.objects.get(id=groupId)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        group.members.add(user)
        group.save()
        serializer = GroupSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LeaveGroup(APIView):
    """
    Leave the group
    """
    def delete(self, request, groupId):
        user = request.user

        try:
            group = Group.objects.get(id=groupId)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            
        res = group.members.remove(user)
        if res == -1:
            print('non')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        group.save()

        if group.members.count() == 0:
            group.delete()
        return Response(status=status.HTTP_200_OK)