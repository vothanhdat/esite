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

class Agency(models.Model):
    agency_name = models.CharField(max_length=100,null=True, blank=True)
    agency_id = models.CharField(max_length=20,null=True, blank=True)
    agency_member = models.ManyToManyField(
        BaseUser,
        through='AgencyMember',
        through_fields=('agency', 'user'),
    )

class AgencyMember(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    inviter = models.ForeignKey(BaseUser, on_delete=models.CASCADE,related_name="membership_invites",null=True)



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
    product_agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    def __str__(self):
        return self.product_name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None)
    image = models.ImageField(upload_to='prjimages/%Y/%m/%d/%H/%M/%S/')
    def __str__(self):
        return self.image.__str__()
