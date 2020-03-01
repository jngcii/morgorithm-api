from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, Group

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=32,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class GroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
        max_length=255,
        validators=[UniqueValidator(queryset=Group.objects.all())]
    )
    members = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'members')