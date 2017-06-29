import moneyed
from djmoney.models.fields import MoneyField
from django.db import models
from django.utils.text import *
from django.utils.encoding import python_2_unicode_compatible



class Cagetory(models.Model):
    cagetory_name = models.CharField(max_length=50)
    cagetory_parent = models.ForeignKey(
        'self',
        null=True,
        blank=True
    )
    def __str__(self):
        return self.cagetory_name

class Brand(models.Model):
    brand_name = models.CharField(max_length=100)
    brand_sym = models.CharField(max_length=20)
    def __str__(self):
        return self.brand_name

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_cagetory = models.ForeignKey(Cagetory)
    product_branch = models.ForeignKey(Brand)
    product_price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    
    def __str__(self):
        return self.product_name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None)
    image = models.ImageField(upload_to='prjimages/%Y/%m/%d/%H/%M/%S/')
    def __str__(self):
        return self.image.__str__()
