from django.db import models
from users.models import User
from problems.models import OriginProb
from django.contrib.humanize.templatetags.humanize import naturaltime

class TimeStampedModel(models.Model):
    """
    model of checking created, updated time
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Solution(TimeStampedModel):
    """
    model of solution
    """
    LANG_CHOICES = (
        ('c', 'c'),
        ('cpp', 'cpp'),
        ('java', 'java'),
        ('python', 'python'),
        ('javascript', 'javascript'),
    )

    problem = models.ForeignKey(OriginProb, on_delete=models.CASCADE, related_name='solutions')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solutions')
    code = models.TextField()
    lang = models.CharField(max_length=255, choices=LANG_CHOICES)
    caption = models.TextField(null=True, blank=True)
    view = models.IntegerField(default=0)
    solved = models.BooleanField()

    @property
    def natural_time(self):
        return naturaltime(self.created_at)
    

class Comment(TimeStampedModel):
    """
    model of comment
    """
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name='comments')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField()

    @property
    def natural_time(self):
        return naturaltime(self.created_at)