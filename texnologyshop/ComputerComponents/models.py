from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from smart_selects.db_fields import ChainedForeignKey
from django.contrib.auth.models import User
# Create your models here.
class Stock(models.Model): # местоположение склада
    location = models.CharField(max_length=255)

class Category(models.Model): # категория товара
    name = models.CharField(max_length=255, unique=True)
    name_ru = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name_ru


class SubCategory(models.Model): # информация о подкатегории товара
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    name_ru = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name_ru

class Product(models.Model): # информация о продукте
    name = models.CharField(max_length=255, unique=True)
    name_ru = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = ChainedForeignKey(
        SubCategory,
        chained_field="category",
        chained_model_field="category",
        show_all=False,
        auto_choose=True,
        sort=True,
        null=True,
        blank=True,
    )
    price = models.PositiveIntegerField()
    content = models.TextField(max_length=1000)
    firm = models.CharField(max_length=255)
    image = models.ImageField(upload_to='imagedb/', null=True, max_length=255, validators=[
        FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif'])])
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)


class Product_Stock(models.Model): # связь двух таблиц, где хранится товар, его информация и количество товара на складе
    count_product = models.IntegerField()
    id_stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Basket(models.Model): # корзина товаров пользователя
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | {self.product.name} '


# class OrderStatus(models.Model): # Под сомнением нужен ли он или нет
#     name = models.CharField(max_length=255, unique=True)
#     name_ru = models.CharField(max_length=255, unique=True)
#
#     def __str__(self):
#         return self.name_ru


class Order(models.Model): # таблица по заказам, здесь храниться информация о купленном товаре
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, default='Не оплачен') #models.ForeignKey(OrderStatus, on_delete=models.SET_NULL)
    type_order = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

class OrderProducts(models.Model): # информаци о товаре
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    counter = models.PositiveIntegerField()
    real_price = models.PositiveIntegerField()
