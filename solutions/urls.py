from django.urls import path
from . import views

urlpatterns = [
    path('solution-api/', views.SolutionAPI.as_view(), name='solution-api'),
    path('comment-api/', views.CommentAPI.as_view(), name='comment-api'),
    path('sub-comment-api/', views.SubCommentAPI.as_view(), name='sub-comment-api'),
    path('get-all-questions/', views.GetAllQuestions.as_view(), name='get-all-questions'),
    path('get-problems-solutions/<int:originId>/', views.GetProblemsSolutions.as_view(), name='get-problems-solutions'),
    path('get-problems-questions/<int:originId>/', views.GetProblemsQuestions.as_view(), name='get-problems-questions'),
    path('get-questions/<int:userId>/', views.GetQuestions.as_view(), name='get-questions'),
    path('get-solution/<int:solutionId>/', views.GetSolution.as_view(), name='get-solution'),
    path('view-solution/<int:solutionId>/', views.ViewCount.as_view(), name='view-solution'),
    path('like-solution/<int:solutionId>/', views.LikeSolution.as_view(), name='like-solution'),
    path('unlike-solution/<int:solutionId>/', views.UnlikeSolution.as_view(), name='unlike-solution'),
    path('search-questions/<txt>/', views.SearchQuestions.as_view(), name='search-questions'),
]