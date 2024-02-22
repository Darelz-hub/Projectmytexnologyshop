import requests
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views import View
from django.views.generic.edit import DeleteView
from ComputerComponents.models import Product, Product_Stock, Category, Basket


class MainPage(View): # основная страница при загрузке сайта
    def get(self, request):
        Laptop = get_object_or_404(Category, name="Laptop")
        PC = get_object_or_404(Category, name="PC")
        COMPONENTS = get_object_or_404(Category, name="Components")
        laptops = Product.objects.all().filter(category=Laptop, is_published=True) # ноутбкуки из бд
        pcs = Product.objects.all().filter(category=PC) # Компьютеры из бд
        components = Product.objects.all().filter(category=COMPONENTS) # все компьютерные компоненты из бд
        counts = Product_Stock.objects.all() # количество товара
        data = {'laptops': laptops, 'counts': counts, 'pcs': pcs, 'components': components}
        return render(request,'computercomponents/main.html', data)


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
   def get(self, request, type_product_components):
       if type_product_components == 'components':
           products = Product.objects.all().filter(type_product=type_product_components)
           title = Product.objects.filter(type_product=type_product_components).first()
       else:
            products = Product.objects.all().filter(type_product_components=type_product_components)
            title = Product.objects.filter(type_product_components=type_product_components).first()
       counts = Product_Stock.objects.all()
       data = {'products': products, 'counts': counts, 'title': title}
       return render(request, 'computercomponents/products.html', data)


class Baskets(View):
    def get(self, request):
        baskets = Basket.objects.all().filter(user_id=request.user.id)
        counts = Product_Stock.objects.all()
        return render(request, 'computercomponents/basket.html', {'baskets': baskets, 'counts': counts})

    def post(self, request):
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=int(product_id))
        baskets = Basket.objects.filter(user=request.user, product=product)
        current_page = request.META.get('HTTP_REFERER')
        if not baskets.exists():
            Basket.objects.create(user=request.user, product=product, quantity=1)
            return HttpResponseRedirect(current_page)
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()
            return HttpResponseRedirect(current_page)

class BasketDelete(View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        current_page = request.META.get('HTTP_REFERER')
        basket = Basket.objects.get(id=product_id)
        basket.delete()
        return HttpResponseRedirect(current_page)

def test(request):
    return render(request, 'testcase/test.html')
