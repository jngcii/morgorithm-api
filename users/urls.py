from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # user (authentication)
    path('', views.UserAPI.as_view(), name='user_api'),
    path('signout/', views.SignOut.as_view(), name='signout'),
    path('change_password/', views.ChangePassword.as_view(), name='change_password'),
    path('profile_image/', views.AvatarAPI.as_view(), name='avatar_api'),

    # user (not-authentication)
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('check_unique/', views.CheckUnique.as_view(), name='check_unique'),

    # group
    path('group/', views.GroupAPI.as_view(), name='group_api'),
    path('group/<int:group_id>/', views.GroupDetailAPI.as_view(), name='group_detail_api'),
    path('group/<int:group_id>/enter/', views.EnterGroup.as_view(), name='enter_group'),
    path('group/<int:group_id>/leave/', views.LeaveGroup.as_view(), name='leave_group'),
]