from django.conf.urls import url
from . import views

urlpatterns = [
    url('api/users/', views.UserCreate.as_view(), name='user-create'),
]