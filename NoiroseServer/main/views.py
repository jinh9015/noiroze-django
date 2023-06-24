from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count
from django.core.paginator import Paginator

from .models import *
from .forms import ComplainBoardForm

# Create your views here.
def base_request(request):
    return render(request, 'base.html')

def dash_request(request):
    return render(request, 'dash.html')





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
    커뮤니티 게시판 리스트 출력
    '''
    
    # 입력 인자
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬 기준 / default 최신순

    # 정렬 기준에 따라 게시물을 가져옴
    if so == 'recent':
        board_list = CommunityBoard.objects.order_by('-created_date')
    elif so == 'late':
        board_list = CommunityBoard.objects.order_by('created_date')
    elif so == 'recommend':
        board_list = CommunityBoard.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-created_date')
    elif so == 'popular':
        board_list = CommunityBoard.objects.annotate(num_reply=Count('reply')).order_by('-num_reply', '-created_date')
    else:
        board_list = CommunityBoard.objects.order_by('-id')

    # 검색어에 따라 필터링
    if kw:
        kw = kw.replace('년', '')
        kw = kw.replace('월', '')
        kw = kw.replace('일', '')
        board_list = board_list.filter(
    Q(title__icontains=kw) |  # 제목 검색
    Q(content__icontains=kw) |  # 내용 검색
    Q(author__name__icontains=kw)  # 작성자 검색
    ).distinct()


    paginator = Paginator(board_list, 10)  # 페이지당 10개
    page_obj = paginator.get_page(page)
    context = {'board_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'board/question_list.html', context)



def question_create(request):
    '''
    질문 생성 폼 및 처리
    '''
    if request.method == 'POST':
        form = ComplainBoardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:community_board_list')
    else:
        form = ComplainBoardForm()

    context = {'form': form}
    return render(request, 'question_create.html', context)



