import json
import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LogInSerializer, GroupSerializer, InitialProfileSerializer
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
                new_serializer = InitialProfileSerializer(user)
                new_json = new_serializer.data
                new_json['token'] = token.key
                return Response(new_json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignIn(APIView):
    """
    Log user in
    """
    permission_classes = [AllowAny]

    def get_user(self, request):
        email = request.data['email']
        password = request.data['password']
        try:
            user = User.objects.get(email=email)
            if user and user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def post(self, request):
        if 'email' not in request.data and 'username' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif 'username' in request.data:
            try:
                email = User.objects.get(username=request.data['username']).email
            except User.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        request.data['email'] = email
        serializer = LogInSerializer(data=request.data)

        if serializer.is_valid():
            user = self.get_user(request)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                new_serializer = InitialProfileSerializer(user)
                new_json = new_serializer.data
                new_json['token'] = token.key
                return Response(new_json, status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    """
    Password Change
    """

    def post(self, request):
        user = request.user

        old_pw = request.data.get('old_password', None)
        new_pw = request.data.get('new_password', None)

        if old_pw is None or new_pw is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        old_check = user.check_password(old_pw)
        
        if not old_check:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if len(new_pw) < 8 or len(new_pw) > 25:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_pw)
        return Response(status=status.HTTP_200_OK)


class CreateGroup(APIView):
    """ 
    Creates the group
    """
    def post(self, request):
        """
        request data
        - name
        """
        user = request.user
        if user.group.count() >= 5:
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
    def post(self, request, groupId):
        user = request.user

        try:
            group = Group.objects.get(id=groupId)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if group.password:
            if not request.data.get('password', None):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if group.password != request.data['password']:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        group.members.add(user)
        group.save()
        serializer = GroupSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LeaveGroup(APIView):
    """
    Leave the group
    """
    def get(self, request, groupId):
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


class SearchGroup(APIView):
    """
    Search the group
    """
    def get(self, request, txt):
        try:
            groups = Group.objects.filter(name__icontains=txt)[:10]
        except Group.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GoogleLoginView(APIView):

    def get(self, request):

        google_access_code = request.GET.get('code', None)

        url = 'https://kauth.kakao.com/oauth/token'

        headers = {
            'Content-type': 'application/x-www-urlencoded; charset=utf-8'
        }
        body = {
            'grant_type': 'authorization_code',
            'client_id': 'aghlasdf',
            'redirect_uri': 'http://localhost',
            'code': google_access_code
        }

        token_google_reponse = requests.post(url, headers=headers, data=body)
        access_token = json.loads(token_google_reponse.text).get('access_token')

        url = 'https://kapi.kakao.com/v2/user/me'

        headers = {
            'Authorization': 'Bearer {}'.format(access_token),
            'Content-type': 'application/x-www-urlencoded; charset=utf-8'
        }

        google_response = requests.get(url, headers=headers)
        google_res = json.loads(google_response.text)

        return Response(status=status.HTTP_200_OK)