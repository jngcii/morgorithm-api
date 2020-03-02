from django.conf.urls import url
from . import views

urlpatterns = [
    url('sign-up/', views.SignUp.as_view(), name='sign-up'),
    url('sign-in/', views.SignIn.as_view(), name='sign-in'),
    url('create-group/', views.CreateGroup.as_view(), name='create-group'),
]