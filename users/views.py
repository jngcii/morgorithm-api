from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from .serializers import SignUpSerializer, UserSerializer, GroupSerializer
from .models import User, Group
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
# from django.template import loader
# from django.core.mail import send_mail
# from django.conf import settings
# from pprint import pprint


def get_group(group_id):
    try:
        group = Group.objects.get(id=group_id)
        return group
    except Group.DoesNotExist:
        return None


class UserAPI(APIView):
    def get(self, request):
        username = request.GET.get('username', None)
        if username:
            user = User.objects.get(username=username)
        else:
            user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        password = request.data.get('password', None)
        if not password or not user.check_password(password):
            return Response(status.HTTP_400_BAD_REQUEST)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SignUp(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        request data
        - username
        - name (option)
        - password
        """
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                login(request, user)
                token = Token.objects.create(user=user)
                response = serializer.data
                response['token'] = token.key
                return Response(response, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class SignIn(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        request data
        - username
        - password
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(**request.data)
            if user:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                response = serializer.data
                response['token'] = token.key
                return Response(response, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SignOut(APIView):
    def get(self, request):
        user = request.user
        token = Token.objects.filter(user=user)
        token.delete()
        logout(request)
        return Response(status=status.HTTP_200_OK)


class ChangePassword(APIView):
    def post(self, request):
        """
        request data
        - password
        """
        user = request.user
        if not 'password' in request.data or len(request.data['password']) < 8:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user.set_password(request.data['password'])
        return Response(status=status.HTTP_200_OK)


class AvatarAPI(APIView):

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        user = request.user
        user.avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CheckUnique(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        request data
        - username
        """
        if 'username' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            User.objects.get(username=request.data['username'])
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_200_OK)


class GroupAPI(APIView):
    def get(self, request):
        keyword = request.GET.get('keyword', None)
        if keyword:
            groups = Group.objects.filter(name__icontains=keyword)[:10]
        else:
            groups = Group.objects.all()[:10]
        serializer = GroupSerializer(groups, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        request data
        - name
        - password (option)
        """
        user = request.user
        serializer = GroupSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            group = serializer.save()
            if group:
                group.members.add(user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class GroupDetailAPI(APIView):
    def get(self, request, group_id):
        group = get_group(group_id)
        if not group:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = GroupSerializer(group, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class EnterGroup(APIView):
    def post(self, request, group_id):
        user = request.user
        group = get_group(group_id)
        if not group:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if group.password:
            password = request.data.get('password', None)
            if not password:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if group.password != password:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        group.members.add(user)
        serializer = GroupSerializer(group, context={"request":request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class LeaveGroup(APIView):
    """
    Leave the group
    """
    def get(self, request, group_id):
        user = request.user
        group = get_group(group_id)
        if not group:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        group.members.remove(user)
        if group.members.count() == 0:
            group.delete()
        return Response(status=status.HTTP_200_OK)




# class SendNewPassword(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):
#         """
#         request data
#         - email
#         """
#         if 'email' not in request.data:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         to_mail_addr = request.data['email']
#         try:
#             user = User.objects.get(email=to_mail_addr)
#         except User.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         code = random.sample('abcdefghijklmnopqrstuvwxyz1234567890', 8)
#         code = ''.join(code)
#         user.set_password(code)
#         user.save()
#         title = '[MORGORITHM] initialize password'
#         from_mail_addr = settings.DEFAULT_FROM_EMAIL
#         html_msg = loader.render_to_string('new_password.html', {'code': code})
#         res = send_mail(
#             title,
#             '',
#             from_mail_addr,
#             [to_mail_addr],
#             fail_silently=True,
#             html_message=html_msg
#         )
#         if res:
#             return Response(status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
