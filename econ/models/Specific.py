from django.db import models
from .Cagetory import Cagetory
from .Product import Product
from .ProductOption import ProductOption

class Specific(models.Model):
    specific_name = models.CharField(max_length=50)
    specific_of = models.ForeignKey(Cagetory,on_delete=models.CASCADE)
    def __str__(self):
        return  self.specific_name
    class Meta:
        unique_together = ("specific_name", "specific_of")



class SpecificDetail(models.Model):
    detail_field = models.ForeignKey(Specific,on_delete=models.CASCADE)
    detail_value = models.CharField(max_length=50,null=True,blank=True)
    class Meta:
        unique_together = ("detail_field", "detail_value")
    def __str__(self):
        return self.detail_value


class ProductSpecDetail(models.Model):
    # specof = models.ForeignKey(Specific)
    spec = models.ForeignKey(SpecificDetail,on_delete=models.CASCADE)
    desc = models.CharField(max_length=100,null=True,blank=True)
    prod = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    prod_option = models.ForeignKey(ProductOption,on_delete=models.CASCADE,null=True,blank=True)
    class Meta:
        unique_together = ("prod","prod_option")


    def __str__(self):
        return self.spec.detail_value
        
    def specof(self):
        if self.spec_id:
            return self.spec.detail_field
        else:
            return None