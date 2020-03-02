from django.conf.urls import url
from . import views

urlpatterns = [
    url('add-origin-prob/', views.AddOriginProb.as_view(), name='add-origin-prob'),
    url('copy-and-get-probs/', views.CopyAndGetProbs.as_view(), name='copy-and-get-probs'),
]