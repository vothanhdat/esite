import moneyed
from djmoney.models.fields import MoneyField
from django.db import models
from django.utils.text import *
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from abc import ABCMeta, abstractmethod


class BaseUser(User):
    GENDER = (
        ('U','Unknow'), 
        ('M','Male'), 
        ('F','Female'), 
    )
    baseuser_bio = models.TextField(max_length=500, blank=True)
    baseuser_address = models.TextField(max_length=500, blank=True)
    baseuser_birthday = models.DateField(null=True, blank=True)
    baseuser_gender = models.CharField(max_length=1, choices=GENDER,default='U')
    baseuser_avatar = models.ImageField(upload_to='media/%Y/%m/%d/%H/%M/%S/',null=True, blank=True)



class Agency(models.Model):
    agency_name = models.CharField(max_length=100,null=True, blank=True)
    agency_id = models.CharField(max_length=20,null=True, blank=True)
    agency_logo = models.ImageField(upload_to='media/%Y/%m/%d/%H/%M/%S/',null=True, blank=True)
    agency_member = models.ManyToManyField(
        BaseUser,
        through='AgencyMember',
        through_fields=('agency', 'user'),
    )
    def __str__(self):
        return self.agency_name


class Promotion(models.Model) : 
    PROMOTION_TYPE = (
        ('M','Minus'), 
        ('P','Percentage'), 
        ('O','Offer'), 
    )
    promotion_name = models.CharField(max_length=100)
    promotion_type = models.CharField(max_length=1, choices=PROMOTION_TYPE,default='P')
    promotion_value = models.FloatField()
    promotion_start = models.DateTimeField(null=True)
    promotion_end = models.DateTimeField(null=True)
    # promotion_agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    class Meta:
        abstract = True

    def __str__(self):
        return self.promotion_name


class AgencyPromotion(Promotion):
    apply_to = models.ForeignKey(Agency, on_delete=models.CASCADE)
    

class AgencyMember(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    inviter = models.ForeignKey(BaseUser, on_delete=models.CASCADE,related_name="membership_invites",null=True, blank=True)



class Cagetory(models.Model):
    cagetory_name = models.CharField(max_length=50)
    cagetory_parent = models.ForeignKey(
        'self',
        null=True,
        blank=True
    )
    def __str__(self):
        return self.cagetory_name

    def paths(self):
        current_cagetory = self
        paths = [current_cagetory,]
        while current_cagetory.cagetory_parent :
            current_cagetory = current_cagetory.cagetory_parent
            paths.append(current_cagetory)
        paths.reverse()
        return paths

    def allproducts(self):
        allprod = self.product_set.all()

        for child_cagetory in self.cagetory_set.all():
            allprod = allprod | child_cagetory.allproducts()
        
        return allprod

    def allspecific(self):
        allspec = ProductSpecific.objects.none()
        for cagetory in self.paths():
            allspec = allspec | cagetory.productspecific_set.all()
        return allspec


    def allproductsdetails(self):
        alldetails = ProductSpecificDetail.objects.none()

        for spec in self.allspecific():
            alldetails = alldetails | spec.productspecificdetail_set.all()

        return alldetails
                


class Brand(models.Model):
    brand_name = models.CharField(max_length=100)
    brand_sym = models.CharField(max_length=20)
    brand_logo = models.ImageField(upload_to='media/%Y/%m/%d/%H/%M/%S/',null=True, blank=True)
    def __str__(self):
        return self.brand_name


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_cagetory = models.ForeignKey(Cagetory)
    product_branch = models.ForeignKey(Brand)
    product_price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    product_agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    product_quatity = models.IntegerField(verbose_name='numbers',default=0)
    product_detail = models.ManyToManyField('ProductSpecificDetail')
    def __str__(self):
        return self.product_name

class ProductPromotion(Promotion) : 
    apply_to = models.ManyToManyField(Product,null=True,blank=True)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None)
    image = models.ImageField(upload_to='media/%Y/%m/%d/%H/%M/%S/')
    def __str__(self):
        return self.image.__str__()



class ProductSpecific(models.Model):
    specific_name = models.CharField(max_length=50)
    specific_unit = models.CharField(max_length=20,null=True,blank=True)
    specific_of = models.ForeignKey(Cagetory,on_delete=models.CASCADE)
    def __str__(self):
        return  self.specific_name

class ProductSpecificDetail(models.Model):
    detail_field = models.ForeignKey(ProductSpecific,on_delete=models.CASCADE)
    detail_value = models.CharField(max_length=50)
    detail_desc = models.CharField(max_length=200,null=True,blank=True)
    def __str__(self):
        return "%s : %s" % (self.detail_field,self.detail_value)
        # self.detail_field.__str__() + ' : ' + self.detail_value.__str__() 

