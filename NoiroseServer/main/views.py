from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count
from django.core.paginator import Paginator

from .models import *

# Create your views here.
def base_request(request):
    return render(request, 'main/base.html')

# 녹음파일 서버에 저장하는 함수
@csrf_exempt
def download_sound_file(request):
    if request.method == 'POST':
        dong = request.POST['dong']
        ho = request.POST['ho']
        file_name = request.POST['file_name']
        sound_file = request.FILES['sound_file']
        model = models.Sound_File(dong=dong, ho=ho, file_name=file_name, sound_file=sound_file)
        model.save()

        print('Downloaded sound file:', dong, ho, file_name, sound_file)
        msg = {'result': 'success'}

    else:
        msg = {'result': 'fail'}

    return JsonResponse(msg)


def community_board_list(request):
    '''
    board_list 출력
    '''
    
    # 입력 인자
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent') # 정렬 기준 / default 최신순

    if so == 'recent':
        board_list = CommunityBoard.objects.order_by('-create_date')
    elif so == 'late':
        board_list = CommunityBoard.objects.order_by('create_date')
    elif so == 'recommend':
        board_list = CommunityBoard.objects.annotate(
            num_voter = Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        board_list = CommunityBoard.objects.annotate(
            num_reply = Count('reply')).order_by('-num_reply', '-create_date')
    else : # 위 경우 제외 board_id 역순정렬
        board_list = CommunityBoard.objects.order_by('-id')

    if kw:
        kw = kw.replace('년','')
        kw = kw.replace('월','')
        kw = kw.replace('일','')
        board_list = board_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(author__name__icontains=kw) |  # 작성자 검색
            Q(club__name__icontains=kw) |    # 클럽 이름 검색
            Q(club__category__icontains=kw) |  # 클럽 카테고리 검색
            Q(event_date__icontains=kw)      # 모임일 검색
        ).distinct()

    paginator = Paginator(board_list, 10)  # 페이지당 10개 
    page_obj = paginator.get_page(page)
    context = {'board_list':page_obj, 'page':page, 'kw':kw, 'so':so}
    return render(request, 'community_board.html')



def dong_101_request(request):
    return render(request, 'main/전체 동/dong_101.html')

def dong_102_request(request):
    return render(request, 'main/전체 동/dong_102.html')

def dong_103_request(request):
    return render(request, 'main/전체 동/dong_103.html')

def dong_104_request(request):
    return render(request, 'main/전체 동/dong_104.html')

def dong_105_request(request):
    return render(request, 'main/전체 동/dong_105.html')         # 동 별 차트를 그리는 페이지로 render 하는 함수