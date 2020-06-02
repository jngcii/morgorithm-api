from rest_framework import serializers
from .models import OriginProb, ProblemGroup, Problem


class OriginProbSerializer(serializers.ModelSerializer):
    level = serializers.IntegerField(allow_null=True, default=None)
    url = serializers.URLField(required=True)
    number = serializers.IntegerField(allow_null=True, required=False, default=None)
    category = serializers.CharField(max_length=255)
    title = serializers.CharField(max_length=255, required=True)
    remark = serializers.CharField(max_length=255, required=False, allow_null=True)


    class Meta:
        model = OriginProb
        fields = ('id', 'level', 'url', 'number', 'category', 'title', 'remark',)


class ProbSerializer(serializers.ModelSerializer):
    origin = OriginProbSerializer()
    is_solved = serializers.BooleanField(default=False)
    solved_time = serializers.DateTimeField(allow_null=True, default=None)
    
    class Meta:
        model = Problem
        fields = ('id', 'origin', 'is_solved', 'solved_time',)


class ProbGroupSerializer(serializers.ModelSerializer):
    problems = serializers.PrimaryKeyRelatedField(
        read_only=True,
        required=False,
        many=True
    )

    class Meta:
        model = ProblemGroup
        fields = ('id', 'name', 'problems', 'problems_count', 'solved_problems_count',)