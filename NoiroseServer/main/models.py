from django.db import models

# Create your models here.

# 사운드 센서 층간소음 측정
class Sound_Level(models.Model):
    DONG_CHOICES = (
        ('A', 'A동'),
        ('B', 'B동'),
        ('C', 'C동'),
        ('D', 'D동'),
        ('E', 'E동'),
    )
    dong = models.CharField(max_length=10, choices=DONG_CHOICES, default='A')
    ho = models.CharField(max_length=4, default=0000)             # 호수 필드 추가
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
        ('A', 'A동'),
        ('B', 'B동'),
        ('C', 'C동'),
        ('D', 'D동'),
        ('E', 'E동'),
    )
    dong = models.CharField(max_length=20, choices=DONG_CHOICES, default='A')
    ho = models.CharField(max_length=4, default=0000)             # 호수 필드 추가
    PLACE_CHOICES = (
        ('거실', '거실'),
        ('안방', '안방'),
        ('주방', '주방'),
        ('방1', '방1'),
        ('방2', '방2'),
    )
    place = models.CharField(max_length=10, choices=PLACE_CHOICES, default='거실')       # 음성파일 녹음 장소
    file_name = models.CharField(max_length=40)                # 녹음된 파일 명
    created_at = models.DateTimeField()           # 녹음 날짜-시간



# 층간소음 AI 필터링 후 데이터
class Sound_Level_Verified(models.Model):
    DONG_CHOICES = (
        ('A', 'A동'),
        ('B', 'B동'),
        ('C', 'C동'),
        ('D', 'D동'),
        ('E', 'E동'),
    )
    dong = models.CharField(max_length=10, choices=DONG_CHOICES, default='A')
    ho = models.CharField(max_length=4, default=0000)             # 호수 필드 추가
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