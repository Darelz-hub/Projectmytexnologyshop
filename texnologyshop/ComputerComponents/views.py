from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse('Страница про компоненты')

def videocard(request):
    data = {
        'title': 'Videocard',
        'menu': ['About','Page1','Page3']
    }
    return render(request,'computercomponents/index.html',data)