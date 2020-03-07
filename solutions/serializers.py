from rest_framework import serializers
from .models import Solution, Comment
from users.models import User


class CreatorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'name')


class MiniSolutionSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer()

    class Meta:
        model = Solution
        fields = (
            'id',
            'creator',
            'lang',
            'solved',
            'view',
            'comment_count',
            'like_count',
        )


class CommentSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer(required=False)
    likes = CreatorSerializer(required=False, many=True)
    
    class Meta:
        model = Comment
        fields = (
            'id',
            'solution',
            'creator',
            'message',
            'likes',
            'like_count',
        )


class CommentUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = (
            'id',
            'message',
        )


class SolutionSerializer(serializers.ModelSerializer):
    caption = serializers.CharField(allow_null=True, default=None)
    view = serializers.IntegerField(default=0)
    likes = CreatorSerializer(required=False, many=True)
    comments = CommentSerializer(required=False, many=True)

    class Meta:
        model = Solution
        fields = (
            'id',
            'problem',
            'code',
            'lang',
            'caption',
            'view',
            'solved',
            'likes',
            'like_count',
            'comments',
            'comment_count',
        )


class SolutionUpdateSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=False)
    lang = serializers.CharField(required=False)
    caption = serializers.CharField(required=False, allow_null=True)
    solved = serializers.BooleanField(required=False)

    class Meta:
        model = Solution
        fields = (
            'id',
            'code',
            'lang',
            'caption',
            'solved',
            'like_count',
            'comment_count',
        )