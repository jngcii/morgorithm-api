from django.urls import path
from . import views

urlpatterns = [
    path('solution-api/', views.SolutionAPI.as_view(), name='solution-api'),
    path('view-solution/<int:solutionId>/', views.ViewCount.as_view(), name='view-solution'),
]