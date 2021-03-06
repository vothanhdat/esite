from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from tagging.fields import TagField
from djmoney.models.fields import MoneyField
from ckeditor.fields import RichTextField

# from .Cagetory import Cagetory
from .Brand import Brand
from .Image import Image
from .Promotion import Promotion
from util.abstractmodels import ModifyLog, SlugMixin

class Product(ModifyLog,SlugMixin,models.Model):
    name = models.CharField(max_length=100)
    cagetory = models.ForeignKey('Cagetory')
    branch = models.ForeignKey('Brand')
    tags = TagField()
    spec_types = models.ManyToManyField('Specific')

    # def parent_tags(self):
    #     cagetory = self.cagetory
    #     parents = cagetory.get_ancestors(ascending=False, include_self=True)
    #     tags = Tag.objects.usage_for_queryset(parents)
    #     tags +=  Tag.objects.get_for_object(self.branch)
    #     return tags

    def __str__(self):
        return self.name

    def images(self):
        return [e.url() for e in self.productimage_set.all()]


class ProductImage(Image):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)



class ProductInfo(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    info = RichTextField(null=True, blank=True)

    def __str__(self):
        return self.product.name


class ProductPromotion(Promotion) : 
    apply_to = models.ManyToManyField(Product,null=True,blank=True)

