from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)


class Group(models.Model):
    """
    users' group
    """
    name = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=12, null=True, blank=True)


class MyUserManager(BaseUserManager):
    """
    custom user manager
    """

    def create_user(self, username, email, name='', password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    custom user model
    username, email, name, is_active, is_admin
    username_filed = username
    required = email
    """
    
    username = models.CharField(max_length=11, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=80, null=True, blank=True)
    group = models.ManyToManyField(Group, blank=True, related_name='members')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
