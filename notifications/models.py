from django.db import models
from users.models import User
from solutions.models import Solution, Comment, TimeStampedModel

class Notification(TimeStampedModel):

    TYPE_CHOICES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
    )

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']


    def __str__(self):
        return 'From:{} - To:{}'.format(self.creator, self.to)