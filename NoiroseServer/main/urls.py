from django.urls import path, include
from . import views
from django.views.generic import TemplateView

app_name = 'main'

urlpatterns = [
    path('base/', views.base_request, name='base'),
    path('sound_file/', views.download_sound_file , name='sound_file'),
]