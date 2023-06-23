from django.urls import path, include
from . import views
from django.views.generic import TemplateView

app_name = 'main'

urlpatterns = [
    path('base/', views.base_request, name='base'),
    path('community_board_list/', views.community_board_list, name='community_board_list'),
    path('sound_file/', views.download_sound_file , name='sound_file'),
    path('dong_101/', views.dong_101_request, name='dong_101'),
    path('dong_102/', views.dong_102_request, name='dong_102'),
    path('dong_103/', views.dong_103_request, name='dong_103'),
    path('dong_104/', views.dong_104_request, name='dong_104'),
    path('dong_105/', views.dong_105_request, name='dong_105'),            # 동별 차트를 그리기 위한 함수의 url
]

# 게시판 html로 이동하는 url 필요 또는, base.html에 게시판 띄우는 작업 필요