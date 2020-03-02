from django.conf.urls import url
from . import views

urlpatterns = [
    url('add-origin-prob/', views.AddOriginProb.as_view(), name='add-origin-prob'),
]