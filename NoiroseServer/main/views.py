from django.shortcuts import render
from . import views
from . import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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

        print('download sound file', dong, ho, file_name, sound_file)
        msg = {'result': 'success'}

    else:
        msg = {'result': 'fail'}

    return JsonResponse(msg)

