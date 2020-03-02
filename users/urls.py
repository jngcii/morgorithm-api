from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.SignUp.as_view(), name='sign-up'),
    path('sign-in/', views.SignIn.as_view(), name='sign-in'),
    path('create-group/', views.CreateGroup.as_view(), name='create-group'),
    path('enter-group/<int:groupId>/', views.EnterGroup.as_view(), name='enter-group'),
]