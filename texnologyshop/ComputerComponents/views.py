from django.http import HttpResponse, Http404
from django.shortcuts import render


# Create your views here.
def index(request):
    return HttpResponse('Страница про компоненты')


def videocard(request):
    data = {
        'title': 'Videocard',
        'menu': ['About', 'Page1', 'Page3']
    }
    return render(request, 'computercomponents/index.html', data)


def videocardyear(request, year):
    if int(year) > 0:
        return HttpResponse(f'видеокарта {year} года выпуска ')
    else:
        raise Http404('<h1>Ошибка 404</h1>')


def components_pages(request, name_page):
    data = {
        'menu': ['Главная', 'Каталог', 'Товары']
    }
    if name_page in ['info_component', 'seach_component']:
        return render(request, f'computercomponents/{name_page}.html', data)
    return Http404('<h1>Page not found</h1>')


def test(request):
    return render(request, 'testcase/test.html')
