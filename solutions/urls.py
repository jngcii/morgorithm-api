from django.urls import path
from . import views

urlpatterns = [
    path('solution-api/', views.SolutionAPI.as_view(), name='solution-api'),
    path('comment-api/', views.CommentAPI.as_view(), name='comment-api'),
    path('view-solution/<int:solutionId>/', views.ViewCount.as_view(), name='view-solution'),
    path('like-solution/<int:solutionId>/', views.LikeSolution.as_view(), name='like-solution'),
    path('unlike-solution/<int:solutionId>/', views.UnlikeSolution.as_view(), name='unlike-solution'),
]