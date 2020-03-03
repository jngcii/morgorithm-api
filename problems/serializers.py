from rest_framework import serializers
from .models import OriginProb, ProblemGroup, Problem


class OriginProbSerializer(serializers.ModelSerializer):
    level = serializers.IntegerField(allow_null=True, default=None)
    url = serializers.URLField(required=True)
    number = serializers.IntegerField(allow_null=True, default=None)
    category = serializers.CharField(max_length=255)
    title = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = OriginProb
        fields = ('id', 'level', 'url', 'number', 'category', 'title', )


class MiniGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProblemGroup
        fields = ('id', 'name', )


class ProbSerializer(serializers.ModelSerializer):
    origin = OriginProbSerializer()
    is_solved = serializers.BooleanField(default=False)
    solved_time = serializers.DateTimeField(allow_null=True, default=None)
    group = MiniGroupSerializer(read_only=True, many=True)
    
    class Meta:
        model = Problem
        fields = ('id', 'origin', 'is_solved', 'solved_time', 'group', )


class CopyProbSerializer(serializers.ModelSerializer):

    class Meta:
        model = Problem
        fields = ('origin', )