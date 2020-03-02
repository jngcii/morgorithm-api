from rest_framework import serializers
from .models import OriginProb


class OriginProbSerializer(serializers.ModelSerializer):
    level = serializers.IntegerField(allow_null=True, default=None)
    url = serializers.URLField(required=True)
    number = serializers.IntegerField(allow_null=True, default=None)
    category = serializers.CharField(max_length=255)
    title = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = OriginProb
        fields = ('id', 'level', 'url', 'number', 'category', 'title')