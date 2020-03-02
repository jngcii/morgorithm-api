from django.db import models
from users.models import User

# Create your models here.
class OriginProb(models.Model):
    level = models.IntegerField(null=True, blank=True)
    url = models.URLField(max_length=255)
    number = models.IntegerField(null=True, blank=True)
    category = models.CharField(null=True, blank=True, max_length=255)
    title = models.CharField(max_length=255)


class ProblemGroup(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problem_groups')


class Problem(models.Model):
    origin = models.ForeignKey(OriginProb, on_delete=models.CASCADE)
    is_solved = models.BooleanField(default=True)
    solved_time = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problems')
    group = models.ManyToManyField(ProblemGroup, blank=True, related_name='problems')