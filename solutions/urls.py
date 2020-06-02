from django.urls import path
from . import views

app_name = 'solutions'

urlpatterns = [
    path('', views.SolutionAPI.as_view(), name='solution_api'),
    # path('solution-api/', views.SolutionAPI.as_view(), name='solution-api'),
    # path('comment-api/', views.CommentAPI.as_view(), name='comment-api'),
    # path('sub-comment-api/', views.SubCommentAPI.as_view(), name='sub-comment-api'),
    # path('get-all-questions/', views.GetAllQuestions.as_view(), name='get-all-questions'),
    # path('get-comment-likes/<int:commentId>/', views.GetCommentLikes.as_view(), name='get-comment-likes'),
    # path('get-comments/<int:solutionId>/', views.GetComments.as_view(), name='get-comments'),
    # path('get-sub-comments/<int:commentId>/', views.GetSubComments.as_view(), name='get-sub-comments'),
    # path('get-problems-solutions/<int:originId>/', views.GetProblemsSolutions.as_view(), name='get-problems-solutions'),
    # path('get-problems-questions/<int:originId>/', views.GetProblemsQuestions.as_view(), name='get-problems-questions'),
    # path('get-solution/<int:solutionId>/', views.GetSolution.as_view(), name='get-solution'),
    # path('get-solution-counts/<int:solutionId>/', views.GetSolutionCounts.as_view(), name='get-solution-counts'),
    # path('view-solution/<int:solutionId>/', views.ViewCount.as_view(), name='view-solution'),
    # path('like-solution/<int:solutionId>/', views.LikeSolution.as_view(), name='like-solution'),
    # path('like-comment/<int:commentId>/', views.LikeComment.as_view(), name='like-comment'),
    # path('get-questions/<username>/', views.GetQuestions.as_view(), name='get-questions'),
    # path('get-solutions/<username>/', views.GetSolutions.as_view(), name='get-questions'),
    # path('search-questions/<txt>/', views.SearchQuestions.as_view(), name='search-questions'),
]