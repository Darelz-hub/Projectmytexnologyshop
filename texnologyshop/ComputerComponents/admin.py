from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Stock)
admin.site.register(Product_Stock)
admin.site.register(SubCategory)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Basket)