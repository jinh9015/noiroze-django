from django.urls import path, include
from .views import *
from django.views.generic import TemplateView

app_name = 'main'

urlpatterns = [
    path('base/', views.base_request, name='base'),
]