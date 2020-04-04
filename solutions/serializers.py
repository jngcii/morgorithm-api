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
    
    class Meta:
        model = SubComment
        fields = (
            'id',
            'comment',
            'creator',
            'message',
            'like_count',
            'natural_time',
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
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = (
            'id',
            'solution',
            'creator',
            'message',
            'likes',
            'like_count',
            'natural_time',
            'is_liked',
        )

    def get_is_liked(self, obj):
        if 'request' in self.context:
            request = self.context['request']
            if obj in request.user.comment_likes.all():
                return True;
        return False


class CommentUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = (
            'id',
            'message',
        )


class SolutionSerializer(serializers.ModelSerializer):
    caption = serializers.CharField(allow_null=True, default="", required=False)
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


class SolutionCountSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Solution
        fields = (
            'id',
            'view',
            'like_count',
            'comment_count',
            'is_liked',
        )

    def get_is_liked(self, obj):
        if 'request' in self.context:
            request = self.context['request']
            if obj in request.user.solution_likes.all():
                return True;
        return False


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

class CommentLikeSerializer(serializers.ModelSerializer):
    likes = CreatorSerializer(required=False, many=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'like_count',
            'likes',
            'is_liked',
        )

    def get_is_liked(self, obj):
        if 'request' in self.context:
            request = self.context['request']
            if obj in request.user.comment_likes.all():
                return True;
        return False