from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, Group
# from problems.models import ProblemGroup


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=32,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    name = serializers.CharField(required=False)
    password = serializers.CharField(min_length=8, write_only=True)
    avatar = serializers.ImageField(use_url=True, read_only=True)
        
    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'password', 'avatar', )


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    password = serializers.CharField(min_length=8, write_only=True, required=False)
    avatar = serializers.ImageField(use_url=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'password', 'avatar', )


class GroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=Group.objects.all())])
    password = serializers.CharField(max_length=20, write_only=True, required=False)
    members = UserSerializer(read_only=True, many=True, required=False)
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
