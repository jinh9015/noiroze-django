from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'main'

urlpatterns = [

    path('base/', views.base_request, name='base'),
    path('dashboard/', views.dash_request, name='dashboard'),

    # 컴플레인 보드
    path('complain_board_list/', views.complain_board_list, name='complain_board_list'),
    path('update_complain_board/<int:complain_board_id>/', views.update_complain_board, name='update_complain_board'),
    path('delete_complain_board/<int:complain_board_id>/', views.delete_complain_board, name='delete_complain_board'),
    path('create_complain_board/', views.create_complain_board, name='create_complain_board'),
    path('complain_board_detail/<int:pk>/', views.complain_board_detail, name='complain_board_detail'),
    path('add_reply/<int:pk>/', views.add_reply, name='add_reply'),

    path('community_board_list/', views.community_board_list, name='community_board_list'),
    path('create_community_board/', views.create_community_board, name='create_community_board'),

    path('dong_101/', views.dong_101_request, name='dong_101'),
    path('dong_102/', views.dong_102_request, name='dong_102'),
    path('dong_103/', views.dong_103_request, name='dong_103'),
    path('dong_104/', views.dong_104_request, name='dong_104'),
    path('dong_105/', views.dong_105_request, name='dong_105'),
    
    path('sound_file/', views.download_sound_file, name='sound_file'),
]

# 게시판 html로 이동하는 url 필요 또는, base.html에 게시판 띄우는 작업 필요