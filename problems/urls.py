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
    path('group/', views.ProbGroupsAPI.as_view(), name='problem-group-api'),# 모든 그룹 가져오기, 그룹 만들기
    path('group/<int:group_id>/', views.ProbGroupAPI.as_view(), name='problem-group-api'),# 그룹 업데이트(문제 넣고 빼기), 그룹 수정(그룹명), 그룹 삭제
    path('group/<int:group_id>/<int:prob_id>/', views.GetIsIncluding.as_view(), name='is_including_problem'),
]