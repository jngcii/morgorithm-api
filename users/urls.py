from django.urls import path
from . import views

urlpatterns = [
    path('upload-avatar/', views.UploadAvatar.as_view(), name='upload-avatar'),
    path('google-auth/', views.GoogleAuthView.as_view(), name='google-auth'),
    path('check-unique/', views.CheckUnique.as_view(), name='check-unique'),
    path('sign-up/', views.SignUp.as_view(), name='sign-up'),
    path('sign-in/', views.SignIn.as_view(), name='sign-in'),
    path('change-password/', views.ChangePassword.as_view(), name='change-password'),
    path('send-confirm-code/', views.SendConfirmCode.as_view(), name='send-confirm-code'),
    path('edit-profile/', views.EditProfile.as_view(), name='edit-profile'),
    path('create-group/', views.CreateGroup.as_view(), name='create-group'),
    path('get-group/<int:groupId>/', views.GetGroup.as_view(), name='get-group'),
    path('enter-group/<int:groupId>/', views.EnterGroup.as_view(), name='enter-group'),
    path('leave-group/<int:groupId>/', views.LeaveGroup.as_view(), name='leave-group'),
    path('get-user/<username>/', views.GetUser.as_view(), name='get-user'),
    path('search-group/<txt>/', views.SearchGroup.as_view(), name='search-group'),
]