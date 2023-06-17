from django.shortcuts import render
from . import views
from django.http import JsonResponse

# Create your views here.
def base_request(request):
    
    return render(request, 'base.html')

