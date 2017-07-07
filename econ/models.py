import moneyed
from djmoney.models.fields import MoneyField
from django.db import models
from django.utils.text import *
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from abc import ABCMeta, abstractmethod
from mptt.models import MPTTModel, TreeForeignKey


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



class Cagetory(MPTTModel):
    cagetory_name = models.CharField(max_length=50)
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
    )
    def __str__(self):
        return self.cagetory_name

    def paths(self):
        return self.get_ancestors(ascending=False, include_self=True)

    def allproducts(self):
        allcagetory = self.get_descendants(include_self=True)
        return Product.objects.filter(product_cagetory__id__in=allcagetory.values('id'))
        
    def allspecific(self):
        return Specific.objects.filter(specific_of__id__in=self.paths().values('id'))


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
    # product_detail = models.ManyToManyField('SpecificDetail',related_name='product')
    def __str__(self):
        return self.product_name

class ProductPromotion(Promotion) : 
    apply_to = models.ManyToManyField(Product,null=True,blank=True)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None)
    image = models.ImageField(upload_to='media/%Y/%m/%d/%H/%M/%S/')
    def __str__(self):
        return self.image.__str__()



class Specific(models.Model):
    specific_name = models.CharField(max_length=50)
    specific_of = models.ForeignKey(Cagetory,on_delete=models.CASCADE)
    def __str__(self):
        return  self.specific_name
    class Meta:
        unique_together = ("specific_name", "specific_of")

class SpecificDetail(models.Model):
    detail_field = models.ForeignKey(Specific,on_delete=models.CASCADE)
    detail_value = models.CharField(max_length=50)
    def __str__(self):
        return self.detail_value


class ProductSpecDetail(models.Model):
    specof = models.ForeignKey(Specific)
    spec = models.ForeignKey(SpecificDetail,on_delete=models.CASCADE)
    prod = models.ForeignKey(Product,on_delete=models.CASCADE)
    desc = models.CharField(max_length=100,null=True,blank=True)
    class Meta:
        unique_together = ("specof", "prod")
    def __str__(self):
        return  self.spec.__str__()

