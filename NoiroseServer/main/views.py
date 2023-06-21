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

def upload_directory_to_s3(local_directory, bucket_name, s3_directory, s3_client):
    for root, dirs, files in os.walk(local_directory):
        for filename in files:
            local_path = os.path.join(root, filename)
            relative_path = os.path.relpath(local_path, local_directory)
            s3_path = os.path.join(s3_directory, relative_path)
            s3_client.upload_file(local_path, bucket_name, s3_path)
            print(f"Uploaded {local_path} to s3://{bucket_name}/{s3_path}")

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

        print('Downloaded sound file:', dong, ho, file_name, sound_file)
        msg = {'result': 'success'}

        # 저장된 파일을 AWS S3의 'noiroze-noisefile-backup' 버킷에 업로드
        media_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../media/sound_file/2023_06_21/")
        bucket_name = 'noiroze-noisefile-backup'
        s3_directory = 'media/sound_file/2023_06_21/'

        # 모든 media 폴더 내 파일들을 S3 버킷에 업로드
        upload_directory_to_s3(media_directory, bucket_name, s3_directory, s3)
        print('Uploaded files to S3:', media_directory)

    else:
        msg = {'result': 'fail'}

    return JsonResponse(msg)
