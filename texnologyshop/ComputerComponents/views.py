import requests
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


def get_documentation(request):
    # name = requests.GET.get('get_info', 'Central_processing_unit')
    result = {}
    req = requests.post(
        f'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exsentences=10&exlimit=2&titles=Central_processing_unit&explaintext=1&format=json')
    req = req.json()
    indexkey = list(req['query']['pages'])[0]  # Берем ключ, который состоит из цифр в словаре pages
    # print(req['query']['pages'][indexkey])
    result.update({'title': req['query']['pages'][indexkey]['title'],
                   'content': req['query']['pages'][indexkey]['extract']})
    print(result)
    return {'response': result}


def components_pages(request, name_page):
    data = get_documentation(request)
    if name_page in ['info_component', 'seach_component', 'documentation']:
        return render(request, f'computercomponents/{name_page}.html', data)
    return Http404('<h1>Page not found</h1>')


# def components_pages(request, name_page):
#     data = {
#         'menu': ['Главная', 'Каталог', 'Товары']
#     }
#     if name_page in ['info_component', 'seach_component', 'documentation']:
#         return render(request, f'computercomponents/{name_page}.html', data)
#     return Http404('<h1>Page not found</h1>')

def test(request):
    return render(request, 'testcase/test.html')
