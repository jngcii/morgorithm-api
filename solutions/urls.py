from django.urls import path
from . import views

app_name = 'solutions'

urlpatterns = [
    # solution
    path('', views.SolutionAPI.as_view(), name='solution_api'),
    path('<int:solution_id>/', views.SolutionDetailAPI.as_view(), name='solution_detail_api'),
    path('<int:solution_id>/like/', views.LikeSolution.as_view(), name='like_solution'),

    #comment
    path('<int:solution_id>/comments/', views.CommentAPI.as_view(), name='comment_api'),
    path('comments/<int:comment_id>/', views.CommentDetailAPI.as_view(), name='comment_detail_api'),
    path('comments/<int:comment_id>/like/', views.LikeComment.as_view(), name='like_comment'),
]