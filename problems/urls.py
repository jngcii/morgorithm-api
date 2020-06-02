from django.urls import path
from . import views

app_name = 'problems'

urlpatterns = [
    # problem
    path('', views.GetProblemList.as_view(), name='get_problem_list'),
    path('<int:origin_id>/', views.GetSingleProblem.as_view(), name='get_single_problem'),
    path('fetch/', views.Fetch.as_view(), name='fetch'),
    path('init/', views.Init.as_view(), name='init'),

    # problem group
    path('group/', views.ProblemGroupAPI.as_view(), name='problem_group_api'),
    path('group/<int:group_id>/', views.SingleProblemGroupAPI.as_view(), name='single_problem_group_api'),
    
    # path('group/<int:group_id>/<int:prob_id>/', views.GetIsIncluding.as_view(), name='is_including_problem'),
]