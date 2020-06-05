from django.db import models
from django.contrib.auth.models import AbstractUser
from config.file_util import user_directory_path


class Group(models.Model):
    """
    users' group
    """
    name = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=20, null=True, blank=True)

    @property
    def members_count(self):
        return self.members.count()

    @property
    def is_private(self):
        return False if self.password == None else True


class User(AbstractUser):
    """
    """
    
    name = models.CharField(max_length=80, null=True, blank=True)
    avatar = models.ImageField(upload_to=user_directory_path, blank=True, null=True, max_length=1000)
    group = models.ManyToManyField(Group, blank=True, related_name='members')
    last_update = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f'{self.username} ({self.name})'

    @property
    def problems_count(self):
        return self.problems.count()
    
    @property
    def solutions_count(self):
        return self.solutions.filter(solved=True).count()

    @property
    def questions_count(self):
        return self.solutions.filter(solved=False).count()