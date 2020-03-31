from rest_framework import serializers
from .models import Solution, Comment, SubComment
from users.models import User
from problems.serializers import OriginProbSerializer


class CreatorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'name')


class MiniSolutionSerializer(serializers.ModelSerializer):
    problem = OriginProbSerializer()
    creator = CreatorSerializer()

    class Meta:
        model = Solution
        fields = (
            'id',
            'creator',
            'lang',
            'caption',
            'solved',
            'problem',
            'view',
            'comment_count',
            'like_count',
        )


class SubCommentSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer(required=False)
    likes = CreatorSerializer(required=False, many=True)
    
    class Meta:
        model = SubComment
        fields = (
            'id',
            'comment',
            'creator',
            'message',
            'likes',
            'like_count',
        )


class SubCommentUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SubComment
        fields = (
            'id',
            'message',
        )


class CommentSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer(required=False)
    likes = CreatorSerializer(required=False, many=True)
    sub_comments = SubCommentSerializer(required=False, many=True)
    
    class Meta:
        model = Comment
        fields = (
            'id',
            'solution',
            'creator',
            'message',
            'likes',
            'like_count',
            'sub_comments',
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
    creator = CreatorSerializer(required=False, read_only=True)

    class Meta:
        model = Solution
        fields = (
            'id',
            'creator',
            'problem',
            'code',
            'lang',
            'caption',
            'view',
            'solved',
        )


class SolutionDetailSerializer(serializers.ModelSerializer):
    problem = OriginProbSerializer()
    creator = CreatorSerializer(required=False, read_only=True)
    # likes = CreatorSerializer(required=False, many=True)
    # comments = CommentSerializer(required=False, many=True)

    class Meta:
        model = Solution
        fields = (
            'id',
            'creator',
            'problem',
            'code',
            'lang',
            'caption',
            'solved',
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