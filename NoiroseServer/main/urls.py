from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'main'

urlpatterns = [

    path('base/', views.base_request, name='base'),
    path('dashboard/', views.dash_request, name='dashboard'),
    path('question/create/', views.question_create, name='question_create'),  # 수정된 부분

    path('community_board_list/', views.community_board_list, name='community_board_list'),
    path('sound_file/', views.download_sound_file, name='sound_file'),
]

# 게시판 html로 이동하는 url 필요 또는, base.html에 게시판 띄우는 작업 필요