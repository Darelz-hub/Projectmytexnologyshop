import requests
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views import View
from ComputerComponents.models import Product, Product_Stock

# Create your views here.
# def index(request):
#     return HttpResponse('Страница про компоненты')
#
#
# def videocard(request):
#     data = {
#         'title': 'Videocard',
#         'menu': ['About', 'Page1', 'Page3']
#     }
#     return render(request, 'computercomponents/index.html', data)
#

# def videocardyear(request, year):
#     if int(year) > 0:
#         return HttpResponse(f'видеокарта {year} года выпуска ')
#     else:
#         raise Http404('<h1>Ошибка 404</h1>')
#

class MainPage(View): # основная страница при загрузке сайта
    def get(self, request):
        laptops = Product.objects.all().filter(type_product='Laptop', is_published=True) # ноутбкуки из бд
        pcs = Product.objects.all().filter(type_product='pc') # Компьютеры из бд
        components = Product.objects.all().filter(type_product='components') # все компьютерные компоненты из бд
        counts = Product_Stock.objects.all() # количество товара
        data = {'laptops': laptops, 'counts': counts, 'pcs': pcs, 'components': components}
        return render(request, 'computercomponents/main.html', data)


class DocumentationMain(View): # основная страница
    def get(self, request):
        return render(request, 'computercomponents/documentationmain.html')


class Documentation(View):
    def post(self, request):
        # ваша логика для получения данных о фильме из API
        if request.method == 'POST':
            name = request.POST.get('name', 'Central_processing_unit')
            result = {}
            req = requests.post(
                f'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exsentences=10&exlimit=2&titles={name}&explaintext=1&format=json')
            req = req.json()
            indexkey = list(req['query']['pages'])[0]  # Берем ключ, который состоит из цифр в словаре pages
            result.update({'title': req['query']['pages'][indexkey]['title'],
                           'content': req['query']['pages'][indexkey]['extract']})
            return render(request, 'computercomponents/documentation.html', {'response': result})
        return {'response': 'STOP'}

class Products(View):
   def get(self, request, name):
       products = Product.objects.all().filter(type_product_components=name)
       counts = Product_Stock.objects.all()
       title = Products.objects.filter(type_product_components=name).first()
       data = {'products': products, 'counts': counts, 'title': title}
       return render(request, 'computercomponents/products.html', data)





def test(request):
    return render(request, 'testcase/test.html')
