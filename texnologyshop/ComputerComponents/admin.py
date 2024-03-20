from django.contrib import admin
from .models import *
# Register your models here.
# обычная регистрация моделей
# admin.site.register(Stock)
# admin.site.register(Product_Stock)
# admin.site.register(SubCategory)
# admin.site.register(Category)
# admin.site.register(Product)
# admin.site.register(Basket)
# admin.site.register(Order)
# admin.site.register(OrderProducts)
# admin.site.register(Delivery)
# admin.site.register(DeliveryStatus)

@admin.register(Product) # регистрация модели Product и её настройка с помощью декоратора
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name_ru', 'category', 'subcategory', 'price', 'firm', 'time_created', 'time_updated', 'is_published')
    ordering = ['time_created', 'category'] # сортировка


# второй вариант регистрации модели Product и её настройка
#admin.site.register(Product, ProductAdmin)
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'location')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_ru')

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'name_ru')
    ordering = ['category']

@admin.register(Product_Stock)
class Product_StockAdmin(admin.ModelAdmin):
    list_display = ('id_stock', 'id_product', 'count_product')
    ordering = ['id_product', 'id_stock']

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
    ordering = ['user']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_user', 'status', 'type_order', 'address', 'time_created', 'time_updated')
    ordering = ['id','id_user']

@admin.register(OrderProducts)
class OrderProductsAdmin(admin.ModelAdmin):
    list_display = ('id_product', 'id_order', 'counter', 'real_price')
    ordering = ['id_order']

@admin.register(DeliveryStatus)
class DeliveryStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_ru')


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'id_order', 'id_order_products', 'status_delivery',
                    'delivery_date', 'delivery_closing_date', 'time_created', 'time_updated')
    ordering = ['id_order', 'id_user', 'status_delivery']
