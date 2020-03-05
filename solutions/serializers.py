from rest_framework import serializers
from .models import Solution


class SolutionSerializer(serializers.ModelSerializer):
    caption = serializers.CharField(allow_null=True, default=None)
    view = serializers.IntegerField(default=0)
    good = serializers.IntegerField(default=0)

    class Meta:
        model = Solution
        fields = (
            'id',
            'problem',
            'code',
            'lang',
            'caption',
            'view',
            'good',
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
        )