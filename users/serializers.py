from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, Group
from problems.models import ProblemGroup

class SignUpSerializer(serializers.ModelSerializer):
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
        fields = ('id', 'username', 'email', 'name', 'password', )


class LogInSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(min_length=4, write_only=True)
    avatar = serializers.ImageField(use_url=True, required=False)
    
    class Meta:
        model = User
        fields = ('email', 'password', 'avatar')


class GroupUserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'email', 'avatar', )


class GroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
        max_length=255,
        validators=[UniqueValidator(queryset=Group.objects.all())]
    )
    password = serializers.CharField(allow_null=True, max_length=12, default=None, write_only=True, required=False)
    members = GroupUserSerializer(read_only=True, many=True, required=False)
    is_joined = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('id', 'name', 'password', 'members', 'members_count', 'is_private', 'is_joined', )

    def get_is_joined(self, obj):
        if 'request' in self.context:
            request = self.context['request']
            if obj in request.user.group.all():
                return True
        return False


class MiniGroupSerializer(serializers.ModelSerializer):
    is_joined = serializers.SerializerMethodField()
    
    class Meta:
        model = Group
        fields = ('id', 'name', 'members_count', 'is_private', 'is_joined', )

    def get_is_joined(self, obj):
        if 'request' in self.context:
            request = self.context['request']
            if obj in request.user.group.all():
                return True
        return False


class MiniProbGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProblemGroup
        fields = ('id', 'name', 'problems_count', 'solved_problems_count',)


class InitialProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(use_url=True, required=False)
    group = MiniGroupSerializer(many=True, read_only=True)
    problem_groups = MiniProbGroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'name',
            'avatar',
            'is_social',
            'group',
            'problem_groups',
            'problems_count',
            'solved_problems_count',
            'questions_count',
        )


class CurrentUserSerializer(serializers.ModelSerializer):
    group = MiniGroupSerializer(many=True, read_only=True)
    avatar = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'name',
            'avatar',
            'is_social',
            'group',
            'problems_count',
            'solved_problems_count',
            'questions_count',
        )


# class EditProfileSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(
#         required=False,
#         max_length=32,
#         validators=[UniqueValidator(queryset=User.objects.all())]
#     )
#     email = serializers.EmailField(
#         required=False,
#         validators=[UniqueValidator(queryset=User.objects.all())]
#     )
#     name = serializers.CharField(
#         required=False
#     )

#     def update(self, instance, validated_data):
#         if validated_data['username']:
#             instance.username = validated_data.get('username', instance.username)
#         if validated_data['name']:
#             instance.name = validated_data.get('name', instance.name)
#         print(instance, "instance")
#         instance.save()
#         return instance

#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'name', 'password', 'group')


class AvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('avatar', )
