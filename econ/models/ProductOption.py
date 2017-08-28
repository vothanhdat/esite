from django.db import models
from djmoney.models.fields import MoneyField

from .Product import Product
from .Image import Image



class ProductOption(models.Model):
    prod = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')

    
    def prod_details(self):
        return self.productspecdetail_set.all()

    def prod_images(self):
        return self.productoptionimage_set.all()

class ProductOptionImage(Image):
    productoption = models.ForeignKey(ProductOption,on_delete=models.CASCADE)
