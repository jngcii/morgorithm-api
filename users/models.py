from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from config.file_util import user_directory_path


class Group(models.Model):
    """
    users' group
    """
    name = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=12, null=True, blank=True)

    @property
    def members_count(self):
        return self.members.count()

    @property
    def is_private(self):
        return False if self.password == None else True


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
        user.is_staff = True
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
    avatar = models.ImageField(upload_to=user_directory_path, blank=True, null=True, max_length=1000)
    group = models.ManyToManyField(Group, blank=True, related_name='members')
    is_social = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # def has_perm(self, perm, obj=None):
    def has_perm(self):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    # def has_module_perms(self, app_label):
    def has_module_perms(self):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __str__(self):
        return self.username

    @property
    def problems_count(self):
        return self.problems.all().count()
    
    @property
    def solved_problems_count(self):
        return self.solutions.filter(solved=True).all().count()

    @property
    def questions_count(self):
        return self.solutions.filter(solved=False).all().count()