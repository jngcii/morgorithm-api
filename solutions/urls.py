from django.urls import path
from . import views

app_name = 'solutions'

urlpatterns = [
    path('', views.SolutionAPI.as_view(), name='solution_api'),
    path('<int:solution_id>/', views.SolutionDetailAPI.as_view(), name='solution_detail_api'),
    path('<int:solution_id>/like/', views.LikeSolution.as_view(), name='like_solution'),
    path('<int:solution_id>/comments/', views.CommentAPI.as_view(), name='comment_api'),

    # path('like-comment/<int:commentId>/', views.LikeComment.as_view(), name='like-comment'),

    # path('sub-comment-api/', views.SubCommentAPI.as_view(), name='sub-comment-api'),
    # path('get-comment-likes/<int:commentId>/', views.GetCommentLikes.as_view(), name='get-comment-likes'),
    # path('get-sub-comments/<int:commentId>/', views.GetSubComments.as_view(), name='get-sub-comments'),
    # path('search-questions/<txt>/', views.SearchQuestions.as_view(), name='search-questions'),


    # path('get-solution-counts/<int:solutionId>/', views.GetSolutionCounts.as_view(), name='get-solution-counts'),

    # path('get-comments/<int:solutionId>/', views.GetComments.as_view(), name='get-comments'),
    # path('comment-api/', views.CommentAPI.as_view(), name='comment-api'),
]