from rest_framework import serializers
from . import models
from solutions.serializers import CreatorSerializer, SolutionSerializer, CommentSerializer


class NotificationSerializer(serializers.ModelSerializer):

    creator = CreatorSerializer()
    solution = SolutionSerializer(required=False)
    comment = CommentSerializer(required=False)

    class Meta:
        model = models.Notification
        fields = (
            'creator',
            'to',
            'notification_type',
            'solution',
            'comment',
            'message',
        )