from django.urls import path
from . import views

urlpatterns = [
    path('add-solution/', views.SolutionAPI.as_view(), name='solution-api'),
]