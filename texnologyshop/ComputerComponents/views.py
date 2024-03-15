import requests
from django.urls import reverse , reverse_lazy
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.views import View
from django.views.generic.edit import DeleteView
from ComputerComponents.models import (Product, Product_Stock, Category, SubCategory, Basket, Order, OrderProducts,
                                       Delivery,DeliveryStatus)
from django.conf import settings
from yookassa import Configuration, Payment
import uuid
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.http import JsonResponse


Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

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


class Documentation(View): #
    def post(self, request):
        # ваша логика для получения данных о фильме из API
        if request.method == 'POST':
            name = request.POST.get('name', 'Видеокарта')
            result = {}
            req = requests.post(
                f'https://ru.wikipedia.org/w/api.php?action=query&prop=extracts&exsentences=10&exlimit=2&titles={name}&explaintext=10&format=json')

            req = req.json()
            indexkey = list(req['query']['pages'])[0]  # Берем ключ, который состоит из цифр в словаре pages
            result.update({'title': req['query']['pages'][indexkey]['title'],
                           'content': req['query']['pages'][indexkey]['extract']})
            return render(request, 'computercomponents/documentation.html', {'response': result})
        return {'response': 'STOP'}

class Products(View): # получение товара по категориям
   def get(self, request, category):
       category_id = Category.objects.get(name=category)
       products = Product.objects.all().filter(category=category_id)
       title = Product.objects.filter(category=Category.objects.get(name=category)).first()
       counts = Product_Stock.objects.all()
       paginator = Paginator(products, 3)  # Показывать по 3 объектов на странице
       page_number = request.GET.get('page')
       page_obj = paginator.get_page(page_number)
       data = {'products': products, 'counts': counts, 'title': title, 'page_obj': page_obj}
       return render(request, 'computercomponents/products.html', data)

class ProductsSubcategory(View): # класс для получения продуктов по подкатегориям
    def get(self, request, category, subcategory):
        category_id = Category.objects.get(name=category)
        subcategory_id = SubCategory.objects.get(name=subcategory)
        products = Product.objects.all().filter(category=category_id, subcategory=subcategory_id)
        title = Product.objects.filter(category=Category.objects.get(name=category)).first()
        counts = Product_Stock.objects.all()
        paginator = Paginator(products, 3)  # Показывать по 3 объектов на странице
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        data = {'products': products, 'counts': counts, 'title': title, 'page_obj': page_obj}
        return render(request, 'computercomponents/products.html', data)
class Baskets(View): # отображение страницы корзины
    def get(self, request):
        baskets = Basket.objects.all().filter(user_id=request.user.id)
        counts = Product_Stock.objects.all()
        return render(request, 'computercomponents/basket.html', {'baskets': baskets, 'counts': counts})

class BasketAddProduct(View): # добавление товара в карзину
    def post(self, request):
        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            print('--------------------------------')
            print(product_id)
            print('--------------------------------')
            product = Product.objects.get(id=int(product_id))
            baskets = Basket.objects.filter(user=request.user, product=product)
            if not baskets.exists():
                Basket.objects.create(user=request.user, product=product, quantity=1)
                return JsonResponse({'message': 'Товар успешно добавлен'})
            else:
                basket = baskets.first()
                basket.quantity += 1
                basket.save()
                return JsonResponse({'message': 'Товар успешно добавлен'})
        return JsonResponse({'error': 'ERROR'}, status=400)
class BasketDeleteProduct(View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        current_page = request.META.get('HTTP_REFERER')
        basket = Basket.objects.get(id=product_id)
        basket.delete()
        return HttpResponseRedirect(current_page)



class FormOrder(View):
    def post(self, request):
        basket_id = request.POST.get('basket_id')
        basket = Basket.objects.get(id=basket_id)
        return render(request, 'computercomponents/order.html', {'basket': basket})

class CreateOrder(View):
    def post(self, request):
        quantity = int(request.POST.get('quantity'))
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        product_stock = Product_Stock.objects.get(id_product=product_id)
        # заглушка на количество товара
        if product_stock.count_product <= quantity:
            return render(request, 'computercomponents/count_error.html')
        else:
            real_price = product.price * quantity
            type_order = request.POST.get('type_order')
            address = request.POST.get('address')
            order = Order.objects.create(id_user=request.user, status='Не оплачено',type_order=type_order,
                                         address=address)
            order_id = order.id
            order_products = OrderProducts.objects.create(id_product=Product.objects.get(id=product_id), id_order=Order.objects.get(id=order_id), counter=quantity, real_price=real_price)
            return render(request, 'computercomponents/ceal.html', {'order': order, 'order_products': order_products})
class OrderProductsDelete(View):
    def post(self, request):
        order_id = request.POST.get('order_id')
        order_product_id = request.POST.get('order_product_id')
        order = Order.objects.get(id=order_id)
        order_product = OrderProducts.objects.get(id=order_product_id)
        order_product.delete()
        order.delete()
        return HttpResponseRedirect(reverse_lazy('main_page'))
class CealOrder(View):
    def post(self, request):
        # получение данных
        product_id = request.POST.get('product_id')
        order_id = request.POST.get('order_id')
        quantity = int(request.POST.get('quantity'))
        order = Order.objects.get(id=order_id)
        real_price = request.POST.get('real_price')
        # оплата
        idempotence_key = uuid.uuid4()
        currency = "RUB"
        description = 'Товары в корзине'
        payment = Payment.create({
            "amount": {
                    "value": real_price,
                    "currency": currency
            },
            "confirmation": {
                "type": "redirect",
                "return_url": f"http://127.0.0.1:8000/payment_success?order_id={order_id}&product_id={product_id}"
                              f"&quantity={quantity}"
            },
            "capture": True,
            "testing": True,
            "description": description,
        },
                idempotency_key=idempotence_key)
        confirmation_url = payment.confirmation.confirmation_url
        return redirect(confirmation_url)
        # request.build_absolute_uri(reverse(payment_success / f'payment_success', kwargs={'order_id': order_id,
        #                                                                                  'product_id': product_id,
        #                                                                                  'quantity': quantity})),
        # kwargs = {'order_id': order_id,
        #           'product_id': product_id,
        #           'quantity': quantity})),
        # f'payment_success?order_id={order_id}'
        #                                                                  f'&product_id={product_id}&quantity={quantity}'
        # f'payment_success', kwargs = {'order_id': order_id,
        #                               'product_id': product_id, 'quantity': quantity}))
        # БАГ, если спустить строчку return redirect(confirmation_url) в самый низ, то товар изменит статус,
        # вычтиться из склада и добавиться в доставку раньше, чем пройдёт оплата, если оставить здесь,
        # то выше перечисленный код не будет работать, оплата пройдёт(успешно), но статус не обновиться,
        # как выйти из данной ситуации?





class PaymentSuccess(View):
    def get(self, request):
        product_id = request.GET.get('product_id')
        order_id = request.GET.get('order_id')
        quantity = int(request.GET.get('quantity'))
        order = Order.objects.get(id=order_id)
        order.status = 'Оплачено'
        order.save()
        # вычитание товара из склада
        product_stock = Product_Stock.objects.get(id_product=product_id)
        product_stock.count_product -= quantity
        product_stock.save()
        # добавление нового заказа в доставку
        Delivery.objects.create(id_user=User.objects.get(id=request.user.id), id_order=Order.objects.get(id=order_id),
                                        id_order_products=OrderProducts.objects.get(id_order=order_id),
                                        status_delivery=DeliveryStatus.objects.get(name='In stock'))
        return render(request, 'computercomponents/payment_success.html')


# class PaymentFailed(View):
#     def get(self, request):
#         return render(request, 'computercomponents/payment_failed.html')


class PageDelivery(View):
    def get(self, request):
        deliverys = Delivery.objects.all().filter(id_user=request.user)
        data = {'deliverys': deliverys}
        return render(request, 'computercomponents/delivery.html', data)

class PageOrder(View):
    def get(self, request):
        orders = Order.objects.filter(
            id_user=request.user,
            status='Не оплачено'
        ).prefetch_related(
            Prefetch(
                'orderproducts_set',
                queryset=OrderProducts.objects.all().select_related('id_product'),
                to_attr='unpaid_products'
            )
        )
        data = {'orders': orders}
        return render(request, 'computercomponents/pageorder.html', data)


# class Developers(View):
#     def get(self, request):
#         orders = Orders.objects.all().filter(user_id=request.user, status='Оплачен')
#         order_products = OrderProduct.objects
#         return render(request,  'computercomponents/developers.html', {'orders': orders})

# def test(request):
#     return render(request, 'testcase/test.html')








