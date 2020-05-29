from django.db import models
from users.models import User

# Create your models here.
class OriginProb(models.Model):

    TYPE_CHOICES = (
        ('Programmers', 'programmers',),
        ('BaekJoon', 'baekjoon'),
        ('SWEA', 'swea'),
    )

    level = models.IntegerField(null=True, blank=True)
    url = models.URLField(max_length=255)
    number = models.IntegerField(null=True, blank=True)
    category = models.CharField(null=True, blank=True, choices=TYPE_CHOICES, max_length=255)
    title = models.CharField(max_length=255)
    remark = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {} - {} - {}'.format(self.category, self.number, self.title, self.level)


class ProblemGroup(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problem_groups')

    @property
    def problems_count(self):
        return self.problems.count()

    @property
    def solved_problems_count(self):
        return self.problems.filter(is_solved=True).count()


class Problem(models.Model):
    origin = models.ForeignKey(OriginProb, on_delete=models.CASCADE)
    is_solved = models.BooleanField(default=False)
    solved_time = models.DateTimeField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problems')
    group = models.ManyToManyField(ProblemGroup, blank=True, related_name='problems')