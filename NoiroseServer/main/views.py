from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import *
from .forms import ComplainBoardForm
from rest_framework.authtoken.models import Token
from django.contrib import messages
from main.models import ComplainBoard

# Create your views here.
def base_request(request):
    return render(request, 'base.html')

def dash_request(request):
    return render(request, 'dash.html')

# 동 페이지
def dong_101_request(request):
    return render(request, 'board/decibel_dong/dong_101.html')

def dong_102_request(request):
    return render(request, 'board/decibel_dong/dong_102.html')

def dong_103_request(request):
    return render(request, 'board/decibel_dong/dong_103.html')

def dong_104_request(request):
    return render(request, 'board/decibel_dong/dong_104.html')

def dong_105_request(request):
    return render(request, 'board/decibel_dong/dong_105.html')


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
    return render(request, 'board/community_board/community_board_list.html', context)

def create_community_board(request):
    if request.method == 'POST':
        form = ComplainBoardForm(request.POST)
        if form.is_valid():
            new_board = form.save(commit=False)
            # 현재 로그인된 사용자를 author에 저장
            token_key = request.COOKIES.get('auth-token')   # 쿠키에서 토큰 가져오기
            try:
                token = Token.objects.get(key=token_key)    # 토큰으로 사용자 정보 가져오기
            except Token.DoesNotExist:
                messages.error(request, '로그인이 필요합니다.')
                return redirect('/common/login/')
            new_board.author = token.user
            new_board.save()
            return redirect('/main/community_board_list/')
    else:
        form = ComplainBoardForm()
        
    return render(request, 'board/community_board/create_community_board.html', {'form': form})


######### 컴플레인 보드 관련 함수 시작
def create_complain_board(request):
    if request.method == 'POST':
        form = ComplainBoardForm(request.POST)
        if form.is_valid():
            new_board = form.save(commit=False)
            # 현재 로그인된 사용자를 author에 저장
            token_key = request.COOKIES.get('auth-token')   # 쿠키에서 토큰 가져오기
            try:
                token = Token.objects.get(key=token_key)    # 토큰으로 사용자 정보 가져오기
            except Token.DoesNotExist:
                messages.error(request, '로그인이 필요합니다.')
                return redirect('/common/login/')
            new_board.author = token.user
            new_board.save()
            return redirect('/main/complain_board_list/')
    else:
        form = ComplainBoardForm()
        
    return render(request, 'board/complain_board/create_complain_board.html', {'form': form})

def update_complain_board(request, complain_board_id):
    complain_board = get_object_or_404(ComplainBoard, id=complain_board_id)

    if request.method == 'POST':
        form = ComplainBoardForm(request.POST, instance=complain_board)
        if form.is_valid():
            # 현재 로그인된 사용자를 확인
            token_key = request.COOKIES.get('auth-token')   # 쿠키에서 토큰 가져오기

            try:
                token = Token.objects.get(key=token_key)    # 토큰으로 사용자 정보 가져오기
                if token.user == complain_board.author:     # 유효한 사용자 확인
                    updated_board = form.save(commit=False)
                    updated_board.author = token.user
                    updated_board.save()
                    return redirect('/main/complain_board_list/')
                else:
                    messages.error(request, '수정 권한이 없습니다.')
                    return redirect('/main/complain_board_list/')
            except Token.DoesNotExist:
                messages.error(request, '로그인이 필요합니다.')
                return redirect('/common/login/')
    else:
        form = ComplainBoardForm(instance=complain_board)

    return render(request, 'board/complain_board/update_complain_board.html', {'form': form, 'complain_board_id': complain_board_id})
    
def delete_complain_board(request, complain_board_id):
    complain_board = get_object_or_404(ComplainBoard, id=complain_board_id)

    if request.method == 'POST':
        # 현재 로그인된 사용자를 확인
        token_key = request.COOKIES.get('auth-token')  # 쿠키에서 토큰 가져오기

        if token_key:
            try:
                token = Token.objects.get(key=token_key)  # 토큰으로 사용자 정보 가져오기
                if token.user == complain_board.author:   # 유효한 사용자 확인
                    complain_board.delete()
                    return redirect('main:complain_board_list')
                else:
                    messages.error(request, '삭제 권한이 없습니다.')
                    return redirect('/main/complain_board_list/')
            except Token.DoesNotExist:
                messages.error(request, '로그인이 필요합니다.')
                return redirect('/common/login/')
        else:
            messages.error(request, '로그인이 필요합니다.')
            return redirect('/common/login/')

    context = {
        'form': ComplainBoardForm(instance=complain_board)
    }
    return render(request, 'board/complain_board/delete_complain_board.html', context)

def complain_board_list(request):
    '''
    board_list 출력
    '''

    # 입력 인자
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬 기준 / default 최신순

    if so == 'recent':
        board_list = ComplainBoard.objects.order_by('-created_date')
    elif so == 'late':
        board_list = ComplainBoard.objects.order_by('created_date')
    elif so == 'recommend':
        board_list = ComplainBoard.objects.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-created_date')
    elif so == 'popular':
        board_list = ComplainBoard.objects.annotate(
            num_reply=Count('reply')).order_by('-num_reply', '-created_date')
    else:  # 위 경우 제외 board_id 역순정렬
        board_list = ComplainBoard.objects.order_by('-id')

    if kw:
        kw = kw.replace('년', '')
        kw = kw.replace('월', '')
        kw = kw.replace('일', '')
        board_list = board_list.filter(
            Q(title__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(author__name__icontains=kw) |  # 작성자 검색
            Q(club__name__icontains=kw) |  # 클럽 이름 검색
            Q(club__category__icontains=kw) |  # 클럽 카테고리 검색
            Q(event_date__icontains=kw)  # 모임일 검색
        ).distinct()

    paginator = Paginator(board_list, 10)  # 페이지당 10개
    page_obj = paginator.get_page(page)
    context = {'board_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'board/complain_board/complain_board_list.html', context)



def complain_board_detail(request, pk):
    board = get_object_or_404(ComplainBoard, pk=pk)
    return render(request, 'board/complain_board/complain_board_detail.html', {'board': board})

def add_reply(request, pk):
    if request.method == "POST":
        complain_board = get_object_or_404(ComplainBoard, pk=pk)
        content = request.POST['content']

        # 현재 로그인된 사용자를 author에 저장
        token_key = request.COOKIES.get('auth-token')  # 쿠키에서 토큰 가져오기
        try:
            token = Token.objects.get(key=token_key)  # 토큰으로 사용자 정보 가져오기
        except Token.DoesNotExist:
            messages.error(request, '로그인이 필요합니다.')
            return redirect('/common/login/')

        author = token.user

        Reply.objects.create(community_board=complain_board, author=author, content=content)

        return redirect('main:complain_board_detail', pk)

#   컴플레인 보드 관련 함수 끝  #
