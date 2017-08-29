from django.db import models
from .Product import Product
from .ProductOption import ProductOption
from .Customer import Customer
from django.core.exceptions import ValidationError
class CardItem(models.Model):

    prod = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    prod_option = models.ForeignKey(ProductOption,on_delete=models.CASCADE,null=True,blank=True)
    user =  models.ForeignKey(Customer,on_delete=models.CASCADE)
    number = models.IntegerField(default=1)

    def clean(self):
        if (not self.prod_option_id ) == (not self.prod_id):
            raise ValidationError("Either prod or prod_option has value")
        if not self.user_id : 
            raise ValidationError("Empty User")

    def item(self):
        if self.prod_option_id:
            return self.prod_option
        elif self.prod_id:
            return self.prod 
        else:
            return None


    
