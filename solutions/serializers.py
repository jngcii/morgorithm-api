from rest_framework import serializers
from .models import Solution, Comment
from users.models import User
from problems.serializers import OriginProbSerializer


class CreatorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    avatar = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'avatar', 'is_social', )


class SolutionSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer(read_only=True)
    problem = OriginProbSerializer(read_only=True)
    code = serializers.CharField(required=False)
    lang = serializers.CharField(required=False)
    caption = serializers.CharField(required=False)
    solved = serializers.BooleanField(required=False)
    view = serializers.IntegerField(required=False)

    class Meta:
        model = Solution
        fields = (
            'id',
            'code',
            'lang',
            'caption',
            'solved',
            'creator',
            'problem',
            'view',
            'likes_count',
            'comments_count',
        )


class CommentSerializer(serializers.ModelSerializer):
    solution = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    creator = CreatorSerializer(required=False, read_only=True)
    likes = CreatorSerializer(required=False, many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = (
            'id',
            'solution',
            'creator',
            'message',
            'likes',
            'likes_count',
            'natural_time',
            'is_liked',
        )

    def get_is_liked(self, obj):
        if 'request' in self.context:
            request = self.context['request']
            if obj in request.user.comment_likes.all():
                return True
        return False

