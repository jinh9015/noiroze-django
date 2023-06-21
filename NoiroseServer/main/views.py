from django.shortcuts import render
from . import views
from . import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import boto3
import os

aws_access_key = os.environ.get("AKIA5VZTIAOJTNNXWBPI")
aws_secret_key = os.environ.get("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")

# S3 인증 정보 추가
s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

# Create your views here.
def base_request(request):
    
    return render(request, 'base.html')



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

        # 저장된 파일을 AWS S3의 'noiroze-noisefile-backup' 버킷에 업로드
        s3 = boto3.client('s3')
        media_directory = "media/"
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), media_directory, file_name)
        file_key = media_directory + file_name
        s3.upload_file(file_path, 'noiroze-noisefile-backup', file_key)

        print('download sound file', dong, ho, file_name, sound_file)
        msg = {'result': 'success'}

    else:
        msg = {'result': 'fail'}

    return JsonResponse(msg)