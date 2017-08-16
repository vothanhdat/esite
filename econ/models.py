import moneyed
from djmoney.models.fields import MoneyField
from django.db import models
from django.utils.text import *
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from abc import ABCMeta, abstractmethod
from mptt.models import MPTTModel, TreeForeignKey, TreeManager
from django.utils.functional import cached_property
from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from tagging.registry import register
from tagging.fields import TagField
from tagging.models import Tag

# from util.func import memoized_method
# from functools import lru_cache

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

class Image(models.Model):
    class Meta:
         abstract = True
    
    image = models.ImageField(upload_to='media/%Y/%m/%d/%H/%M/%S/',null=True, blank=True)
    image_link = models.CharField(max_length=300,null=True, blank=True)
    
    def __str__(self):
        return self.url()

    def url(self):
        if(self.image):
            return self.image.url
        else :
            return self.image_link


class Agency(models.Model):
    agency_name = models.CharField(max_length=100,null=True, blank=True)
    agency_id = models.CharField(max_length=20,null=True, blank=True)
    agency_logo = models.ImageField(upload_to='media/%Y/%m/%d/%H/%M/%S/',null=True, blank=True)
    agency_member = models.ManyToManyField(
        BaseUser,
        through='AgencyMember',
        through_fields=('agency', 'user'),
    )
    slug = models.SlugField(unique=True,null=True, blank=True)
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
    OPTIONS_CHOICES = (
        (1,'Inherit'),
        (2,'Option by specify'),
        (3,'Option by generic'),
    )

    cagetory_name = models.CharField(max_length=50)
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
    )
    tags = TagField()
    slug = models.SlugField(unique=True,null=True, blank=True)

    optiontype = models.IntegerField(choices=OPTIONS_CHOICES, default=1)   

    def option_type(self):
        if self.optiontype == 1 and self.parent_id:
            return self.parent.option_type()
        else :
            return self.optiontype

    def __str__(self):
        return self.cagetory_name

    def paths(self):
        return self.get_ancestors(ascending=False, include_self=True)

    def path_ids(self):
        return self.paths().values('id')

    def allproducts(self):
        allcagetory_ids = self.get_descendants(include_self=True).values('id')
        return Product.objects.filter(product_cagetory__id__in=allcagetory_ids)

    # def parent_tags(self):
    #     parents = self.get_ancestors(ascending=False, include_self=False)
    #     tags = Tag.objects.usage_for_queryset(parents)
    #     return tags
    
    def allspecific(self):
        path_ids = self.path_ids()
        return Specific.objects.filter(specific_of__id__in=path_ids)

    @staticmethod
    def hash():
        return Cagetory.incrementCount 

    def save(self, *args, **kwargs):
        Cagetory.incrementCount += 1
        print ('incrementCount: %s',Cagetory.incrementCount)
        super(Cagetory, self).save(*args, **kwargs) # Call the "real" save() method.

Cagetory.incrementCount = 0

class Brand(models.Model):
    brand_name = models.CharField(max_length=100)
    brand_sym = models.CharField(max_length=20)
    brand_logo = models.ImageField(upload_to='media/%Y/%m/%d/%H/%M/%S/',null=True, blank=True)
    tags = TagField()
    slug = models.SlugField(unique=True,null=True, blank=True)

    def __str__(self):
        return self.brand_name


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_cagetory = models.ForeignKey(Cagetory)
    product_branch = models.ForeignKey(Brand)
    product_price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    product_agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    product_quatity = models.IntegerField(verbose_name='numbers',default=0)
    tags = TagField()
    slug = models.SlugField(unique=True,null=True, blank=True)


    # def parent_tags(self):
    #     cagetory = self.product_cagetory
    #     parents = cagetory.get_ancestors(ascending=False, include_self=True)
    #     tags = Tag.objects.usage_for_queryset(parents)
    #     tags +=  Tag.objects.get_for_object(self.product_branch)
    #     return tags

    def __str__(self):
        return self.product_name

    def images(self):
        return [e.url() for e in self.productimage_set.all()]


class ProductInfo(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    info = RichTextField(null=True, blank=True)

    def __str__(self):
        return self.product.product_name

class ProductPromotion(Promotion) : 
    apply_to = models.ManyToManyField(Product,null=True,blank=True)


class ProductImage(Image):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)


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



class ProductOption(models.Model):
    prod = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')

    
    def prod_details(self):
        return self.productspecdetail_set.all()

    def prod_images(self):
        return self.productoptionimage_set.all()

class ProductOptionImage(Image):
    productoption = models.ForeignKey(ProductOption,on_delete=models.CASCADE)

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



# class TaggedInfo(models.Model):
#     slug = models.SlugField(unique=True)
#     tags = TagField()
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')

#     def __str__(self):              # __unicode__ on Python 2
#         return self.slug

#     def parent_tags(self,instance):


#         if isinstance(instance,Cagetory):
#             ctype = ContentType.objects.get_for_model(Cagetory)
#             parents = instance.get_ancestors(ascending=False, include_self=False)
#             parent_ids = parents.values('id')
#             tags =  TaggedInfo.objects.filter(content_type__pk = ctype.id,object_id__in=parent_ids)
#             return ', '.join([(i.tags) for i in tags])

#         elif isinstance(instance,Product) and instance.product_cagetory_id:
#             cagetory = instance.product_cagetory
#             ctype = ContentType.objects.get_for_model(Cagetory)
#             parents = cagetory.get_ancestors(ascending=False, include_self=True)
#             parent_ids = parents.values('id')
#             tags =  TaggedInfo.objects.filter(content_type__pk = ctype.id,object_id__in=parent_ids)

#             ctype = ContentType.objects.get_for_model(Brand)
#             tags = tags | TaggedInfo.objects.filter(
#                 content_type__pk = ContentType.objects.get_for_model(Brand).id,
#                 object_id=instance.product_branch_id
#             )

#             return ', '.join([(i.tags) for i in tags])

#         else :
#             return ''


# register(TaggedInfo)

