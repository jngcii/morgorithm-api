from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import (
    UserSerializer,
    LogInSerializer,
    MiniGroupSerializer,
    GroupSerializer,
    InitialProfileSerializer,
    CurrentUserSerializer
)
from .models import User, Group
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.template import loader
from django.core.mail import send_mail
from django.conf import settings
import random

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

    def post(self, request):
        if 'email' not in request.data and 'username' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if 'username' in request.data:
            try:
                email = User.objects.get(username=request.data['username']).email
                request.data['email'] = email
            except User.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = LogInSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(email=request.data['email'], password=request.data['password'])
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                new_serializer = InitialProfileSerializer(user)
                new_json = new_serializer.data
                new_json['token'] = token.key
                return Response(new_json, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class GetUser(APIView):
    """
    Get User
    """
    def get(self, request, userId):
        """
        request data 안받는다
        """
        try:
            user = User.objects.get(id=userId)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = CurrentUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


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


class GetGroup(APIView):
    """
    get group
    """
    def get(self, request, groupId):
        """
        not get request data
        """
        try:
            group = Group.objects.get(id=groupId)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = GroupSerializer(group, context={"request":request})
        return Response(serializer.data, status=status.HTTP_200_OK)


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
                new_serializer = GroupSerializer(group, context={"request":request})
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
        serializer = GroupSerializer(group, context={"request":request})
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
        
        serializer = MiniGroupSerializer(groups, many=True, context={"request":request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CheckUnique(APIView):
    """
    Check email unqiue
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        request data
        - username or email
        """
        print(request.data)
        if 'email' in request.data:
            try:
                User.objects.get(email=request.data['email'])
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response(status=status.HTTP_200_OK)
        elif 'username' in request.data:
            try:
                User.objects.get(username=request.data['username'])
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)




class SendConfirmCode(APIView):
    """
    Send Confirm code
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        request data
        - email
        """
        if 'email' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        to_mail_addr = request.data['email']
        if User.objects.filter(email=to_mail_addr).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        code = random.sample('abcdefghijklmnopqrstuvwxyz1234567890', 8)
        code = ''.join(code)

        title = '[MORGORITHM] Confirm email'
        from_mail_addr = settings.DEFAULT_FROM_EMAIL
        html_msg = loader.render_to_string('email_template.html', {'code': code})

        res = send_mail(
            title,
            '',
            from_mail_addr,
            [to_mail_addr],
            fail_silently=False,
            html_message=html_msg
        )

        if res:
            return Response({'confirm_code': code}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ConfirmEmail(APIView):
    """
    Veirfy email
    """
    def get(self, request):
        user = request.user
        user.is_confirmed = True
        user.save()
        return Response(status=status.HTTP_200_OK)
        