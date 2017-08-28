from django.db import models
from .Product import Product
from .ProductOption import ProductOption

class CardItem(models.Model):
    prod = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    prod_option = models.ForeignKey(ProductOption,on_delete=models.CASCADE,null=True,blank=True)