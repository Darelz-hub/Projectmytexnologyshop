from django.db import models


# Create your models here.
class Stock(models.Model):
    location = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    name_ru = models.CharField(max_length=255, unique=True)
    price = models.IntegerField()
    content = models.TextField(max_length=255)
    firm = models.CharField(max_length=255)
    image = models.ImageField(max_length=50, height_field=100, width_field=100)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)


class Product_Stock(models.Model):
    count_product = models.IntegerField()
    id_stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
