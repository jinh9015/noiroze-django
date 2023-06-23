from django.db import models
from django.shortcuts import redirect, render
from common.models import CustomUser
from django.utils import timezone

# Create your models here.

# 사운드 센서 층간소음 측정
class Sound_Level(models.Model):
    DONG_CHOICES = (
        ('101', '101동'),
        ('102', '102동'),
        ('103', '103동'),
        ('104', '104동'),
        ('105', '105동'),
    )
    dong = models.CharField(max_length=10, choices=DONG_CHOICES, default='101')
    HO_CHOICES = (
        ('101', '101호'),
        ('102', '102호'),
        ('201', '201호'),
        ('202', '202호'),
        ('301', '301호'),
        ('302', '302호'),
        ('401', '401호'),
        ('402', '402호'),
        ('501', '501호'),
        ('502', '502호'),
        ('601', '601호'),
        ('602', '602호'),
        ('701', '701호'),
        ('702', '702호'),
        ('801', '801호'),
        ('802', '802호'),
        ('901', '901호'),
        ('902', '902호'),
        ('1001', '1001호'),
        ('1002', '1002호'),
    )
    ho = models.CharField(max_length=5, choices=HO_CHOICES, default='101')             # 호수 필드 추가
    PLACE_CHOICES = (
        ('거실', '거실'),
        ('안방', '안방'),
        ('주방', '주방'),
        ('방1', '방1'),
        ('방2', '방2'),
    )
    place = models.CharField(max_length=10, choices=PLACE_CHOICES, default='거실')       # 센서 설치 장소
    value = models.FloatField()                   # 센서 값 ( dB(A) )
    created_at = models.DateTimeField()           # 측정 날짜-시간



# 층간소음 녹음 파일
class Sound_File(models.Model):
    DONG_CHOICES = (
        ('101', '101동'),
        ('102', '102동'),
        ('103', '103동'),
        ('104', '104동'),
        ('105', '105동'),
    )
    dong = models.CharField(max_length=10, choices=DONG_CHOICES, default='101')
    HO_CHOICES = (
        ('101', '101호'),
        ('102', '102호'),
        ('201', '201호'),
        ('202', '202호'),
        ('301', '301호'),
        ('302', '302호'),
        ('401', '401호'),
        ('402', '402호'),
        ('501', '501호'),
        ('502', '502호'),
        ('601', '601호'),
        ('602', '602호'),
        ('701', '701호'),
        ('702', '702호'),
        ('801', '801호'),
        ('802', '802호'),
        ('901', '901호'),
        ('902', '902호'),
        ('1001', '1001호'),
        ('1002', '1002호'),
    )
    ho = models.CharField(max_length=5, choices=HO_CHOICES, default='101')             # 호수 필드 추가
    PLACE_CHOICES = (
        ('거실', '거실'),
        ('안방', '안방'),
        ('주방', '주방'),
        ('방1', '방1'),
        ('방2', '방2'),
    )
    place = models.CharField(max_length=10, choices=PLACE_CHOICES, default='거실')       # 음성파일 녹음 장소
    value = models.FloatField(null=True)                       # 녹음 측정 시, 그때의 데시벨 측정값.
    file_name = models.CharField(max_length=40)                # 녹음된 파일 명
    sound_file = models.FileField(upload_to="sound_file/%Y_%m_%d", null=True)     # 수신받은 파일이 서버에 저장될 위치
    created_at = models.DateTimeField(auto_now_add=True)           # 녹음 날짜-시간





# 층간소음 AI 필터링 후 데이터
class Sound_Level_Verified(models.Model):
    DONG_CHOICES = (
        ('101', '101동'),
        ('102', '102동'),
        ('103', '103동'),
        ('104', '104동'),
        ('105', '105동'),
    )
    dong = models.CharField(max_length=10, choices=DONG_CHOICES, default='101')
    HO_CHOICES = (
        ('101', '101호'),
        ('102', '102호'),
        ('201', '201호'),
        ('202', '202호'),
        ('301', '301호'),
        ('302', '302호'),
        ('401', '401호'),
        ('402', '402호'),
        ('501', '501호'),
        ('502', '502호'),
        ('601', '601호'),
        ('602', '602호'),
        ('701', '701호'),
        ('702', '702호'),
        ('801', '801호'),
        ('802', '802호'),
        ('901', '901호'),
        ('902', '902호'),
        ('1001', '1001호'),
        ('1002', '1002호'),
    )
    ho = models.CharField(max_length=5, choices=HO_CHOICES, default='101')              # 호수 필드 추가
    PLACE_CHOICES = (
        ('거실', '거실'),
        ('안방', '안방'),
        ('주방', '주방'),
        ('방1', '방1'),
        ('방2', '방2'),
    )
    place = models.CharField(max_length=10, choices=PLACE_CHOICES, default='거실')       # 센서 설치 장소
    value = models.FloatField(null=True)                   # 센서 값 ( dB(A) )
    created_at = models.DateTimeField(null=True)           # 측정 날짜-시간
    sound_type = models.CharField(max_length=100, null=True)  
    file_name = models.CharField(max_length=40, null=True)   # 녹음된 파일 명


class CommunityBoard(models.Model):                            # 커뮤니티 게시판 모델
    CATEGORY_CHOICES = (
        ('정보공유', '정보공유'),
        ('소통해요', '소통해요'),
        ('붙어봐요', '붙어봐요'),
        ('칭찬해요', '칭찬해요'),
        ('나눔해요', '나눔해요'),
    )
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='정보공유')       
    title = models.CharField(max_length=200) 
    content = models.TextField()  
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    

class ComplainBoard(models.Model):                            # 민원접수 게시판 모델
    title = models.CharField(max_length=200) 
    content = models.TextField()  
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

from .models import ComplainBoard
from .forms import ComplainBoardForm

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