from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from smart_selects.db_fields import ChainedForeignKey
from django.contrib.auth.models import User


# Create your models here.
class Stock(models.Model):  # местоположение склада
    location = models.CharField(max_length=255, verbose_name='Местоположение')

    def __str__(self):
        return self.location

    class Meta:
        verbose_name = 'Склад'  # название модели в админ панели единственное число
        verbose_name_plural = 'Склад'  # множественное число


class Category(models.Model):  # категория товара
    name = models.CharField(max_length=255, unique=True, verbose_name='Категория')
    name_ru = models.CharField(max_length=255, unique=True, verbose_name='Категория на русском')

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name = 'Категория товаров'  # название модели в админ панели единственное число
        verbose_name_plural = 'Категория товаров'  # множественное число


class SubCategory(models.Model):  # информация о подкатегории товара
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE,
                                 verbose_name="Категория")
    name = models.CharField(max_length=255, unique=True, verbose_name='Подкатегория')
    name_ru = models.CharField(max_length=255, unique=True, verbose_name='Подкатегория на русском')

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name = 'Подкатегория товаров'  # название модели в админ панели единственное число
        verbose_name_plural = 'Подкатегория товаров'  # множественное число


class Product(models.Model):  # информация о продукте
    name = models.CharField(max_length=255, unique=True, verbose_name='Наименование товара')
    name_ru = models.CharField(max_length=255, unique=True, verbose_name='Наименование товара на русском')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория')
    subcategory = ChainedForeignKey(
        SubCategory,
        chained_field="category",
        chained_model_field="category",
        show_all=False,
        auto_choose=True,
        sort=True,
        null=True,
        blank=True,
        verbose_name='Подкатегория'
    )
    price = models.PositiveIntegerField(verbose_name='Цена')
    content = models.TextField(max_length=1000, verbose_name='Информация')
    firm = models.CharField(max_length=255, verbose_name='Фирма')
    image = models.ImageField(upload_to='imagedb/', null=True, max_length=255, validators=[
        FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif'])], verbose_name='Изображение')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовать')

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name = 'Товары'  # название модели в админ панели единственное число
        verbose_name_plural = 'Товары'  # множественное число


class Product_Stock(models.Model):  # связь двух таблиц, где хранится товар, его информация и количество товара на складе
    count_product = models.PositiveIntegerField(verbose_name='Количество товара')
    id_stock = models.ForeignKey(Stock, on_delete=models.CASCADE, verbose_name="id_склада")
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="id_товара")

    def __str__(self):
        return f' Название товара: {self.id_product.name_ru}, | Местоположение склада {self.id_stock.location} | Количество товара на складе {self.count_product}'

    class Meta:
        verbose_name = 'Количество продуктов на складе'  # название модели в админ панели единственное число
        verbose_name_plural = 'Количество продуктов на складе'  # множественное число


class Basket(models.Model):  # корзина товаров пользователя
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | {self.product.name_ru} '

    class Meta:
        verbose_name = 'Корзина товаров'  # название модели в админ панели единственное число
        verbose_name_plural = 'Корзина товаров'  # множественное число


# class OrderStatus(models.Model): # Под сомнением нужен ли он или нет
#     name = models.CharField(max_length=255, unique=True)
#     name_ru = models.CharField(max_length=255, unique=True)
#
#     def __str__(self):
#         return self.name_ru


class Order(models.Model):  # таблица по заказам, здесь храниться информация о купленном товаре
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="id_пользователя")
    status = models.CharField(max_length=255,
                              default='Не оплачен',
                              verbose_name="Статус заказа")  # models.ForeignKey(OrderStatus, on_delete=models.SET_NULL)
    type_order = models.CharField(max_length=255, verbose_name="Тип доставки")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Время создания заказа")
    time_updated = models.DateTimeField(auto_now=True, verbose_name="Время обновления заказа")

    class Meta:
        verbose_name = 'Заказы'  # название модели в админ панели единственное число
        verbose_name_plural = 'Заказы'  # множественное число

    def __str__(self):
        return str(self.id)
class OrderProducts(models.Model):  # информаци о товаре
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="id_продукта")
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="id_заказа")
    counter = models.PositiveIntegerField(verbose_name="Количество")
    real_price = models.PositiveIntegerField(verbose_name="Итоговая цена")

    def __str__(self):
        return f' Название продукта: {self.id_product.name_ru} | Номер заказа: {self.id_order} | Количество: {self.counter} | Итоговая цена: {self.real_price}'

    class Meta:
        verbose_name = 'Информация о товаре в заказе'  # название модели в админ панели единственное число
        verbose_name_plural = 'Информация о товаре в заказе'  # множественное число


class DeliveryStatus(models.Model): # статус доставки
    name = models.CharField(max_length=255, unique=True, verbose_name='Статус')
    name_ru = models.CharField(max_length=255, unique=True, verbose_name='Статус на русском')

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name = 'Статус доставки'  # название модели в админ панели единственное число
        verbose_name_plural = 'Статус доставки'  # множественное число


class Delivery(models.Model): # доставка
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="id_пользователя")
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="id_заказа")
    id_order_products = models.ForeignKey(OrderProducts, on_delete=models.CASCADE,
                                          verbose_name="id_информации о товаре в заказе")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_updated = models.DateTimeField(auto_now=True, verbose_name="Время добавления")
    delivery_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата доставки")
    delivery_closing_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата закрытия заказа")
    status_delivery = models.ForeignKey(DeliveryStatus, on_delete=models.CASCADE, verbose_name="Статус доставки")

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставка'

    def __str__(self):
        return f'Заказ № {str(self.id_order.id)}'
