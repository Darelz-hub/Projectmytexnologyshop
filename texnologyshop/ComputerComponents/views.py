from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse('Страница про компоненты')

def videocard(request, id_cc):
    return HttpResponse(f'Видео карта {id_cc}')