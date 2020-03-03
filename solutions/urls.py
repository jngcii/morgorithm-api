from django.urls import path
from . import views

urlpatterns = [
    path('add-solution/', views.AddSolution.as_view(), name='add-solution'),
]