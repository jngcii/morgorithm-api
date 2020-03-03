from rest_framework import serializers
from .models import Solution

class SolutionSerializer(serializers.ModelSerializer):
    caption = serializers.CharField(allow_null=True, default=None)
    view = serializers.IntegerField(default=0)

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
        )