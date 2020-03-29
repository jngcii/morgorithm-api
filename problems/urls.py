from django.urls import path
from . import views

urlpatterns = [
    path('add-origin-prob/', views.AddOriginProb.as_view(), name='add-origin-prob'),
    path('copy-and-get-probs/', views.CopyAndGetProbs.as_view(), name='copy-and-get-probs'),
    path('problem-group-api/', views.ProblemGroupAPI.as_view(), name='problem-group-api'),
    path('update-problems-to-group/', views.UpdateProblemsToGroup.as_view(), name='update-problems-to-group'),
    path('get-problems/', views.GetProblems.as_view(), name='get-problems'),
]