from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, Group
from problems.models import ProblemGroup

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


class GroupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'username', 'name', 'email')


class GroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
        max_length=255,
        validators=[UniqueValidator(queryset=Group.objects.all())]
    )
    password = serializers.CharField(allow_null=True, max_length=12, default=None, write_only=True, required=False)
    members = GroupUserSerializer(read_only=True, many=True, required=False)

    class Meta:
        model = Group
        fields = ('id', 'name', 'password', 'members', 'members_count',)


class MiniGroupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Group
        fields = ('id', 'name', 'members_count',)


class MiniProbGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProblemGroup
        fields = ('id', 'name', 'problems_count', 'solved_problems_count',)


class InitialProfileSerializer(serializers.ModelSerializer):
    group = MiniGroupSerializer(many=True, read_only=True)
    problem_groups = MiniProbGroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'name',
            'group',
            'problem_groups',
            'problems_count',
            'solved_problems_count',
            'questions_count',
        )

class CurrentUserSerializer(serializers.ModelSerializer):
    group = MiniGroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'name',
            'group',
            'problems_count',
            'solved_problems_count',
            'questions_count',
        )