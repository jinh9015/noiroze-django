from django.shortcuts import render
from . import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import boto3
import os

aws_access_key = os.environ.get("AWS_ACCESS_KEY")
aws_secret_key = os.environ.get("AWS_SECRET_KEY")

# S3 인증 정보 추가
s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

def upload_file_to_s3(local_file_path, bucket_name, s3_key):
    s3.upload_file(local_file_path, bucket_name, s3_key)
    print(f"Uploaded {local_file_path} to s3://{bucket_name}/{s3_key}")

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

        # 업로드된 파일을 AWS S3의 'noiroze-noisefile-backup' 버킷에 업로드'
        media_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../media/sound_file/2023_06_21/")
        local_file_path = os.path.join(media_directory, file_name)
        bucket_name = 'noiroze-noisefile-backup'
        s3_key = os.path.join('media', 'sound_file', '2023_06_21', file_name)
        upload_file_to_s3(local_file_path, bucket_name, s3_key)

        print('Downloaded sound file:', dong, ho, file_name, sound_file)
        msg = {'result': 'success'}
    else:
        msg = {'result': 'fail'}

    return JsonResponse(msg)