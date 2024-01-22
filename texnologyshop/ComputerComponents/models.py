from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone


# Create your models here.
class Stock(models.Model):
    location = models.CharField(max_length=255)



class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    name_ru = models.CharField(max_length=255, unique=True)
    type_product = models.TextField(max_length=255, default=None)
    price = models.IntegerField()
    content = models.TextField(max_length=1000)
    firm = models.CharField(max_length=255)
    image = models.ImageField(upload_to='imagedb/', null=True, max_length=255, validators=[
        FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif']),
    ])
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)


class Product_Stock(models.Model):
    count_product = models.IntegerField()
    id_stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
