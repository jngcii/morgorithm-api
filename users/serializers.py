from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, Group
from problems.serializers import ProbGroupSerializer, ProbSerializer

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
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'password', 'group')


class LogInSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(min_length=4, write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'password')


class GroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
        max_length=255,
        validators=[UniqueValidator(queryset=Group.objects.all())]
    )
    password = serializers.CharField(allow_null=True, max_length=12, default=None, write_only=True)
    members = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'password', 'members')


class InitialProfileSerializer(serializers.ModelSerializer):
    group = GroupSerializer(many=True, read_only=True)
    problem_groups = ProbGroupSerializer(many=True, read_only=True)
    problems = ProbSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'name',
            'group',
            'problem_groups',
            'problems',
            'is_confirmed',
        )