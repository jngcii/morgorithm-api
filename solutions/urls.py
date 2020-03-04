from django.urls import path
from . import views

urlpatterns = [
    path('solution-api/', views.SolutionAPI.as_view(), name='solution-api'),
]