from django.db import models
from mptt.models import MPTTModel, TreeForeignKey, TreeManager
from django.contrib.contenttypes.fields import GenericRelation
from tagging.fields import TagField
from .ModifyLog import ModifyLog
from .Slug import Slug

class Cagetory(MPTTModel,ModifyLog):
    OPTIONS_CHOICES = (
        (1,'Inherit'),
        (2,'Option by specify'),
        (3,'Option by generic'),
    )

    name = models.CharField(max_length=50)
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
    )
    tags = TagField()
    slug = GenericRelation(Slug)

    optiontype = models.IntegerField(choices=OPTIONS_CHOICES, default=1)   

    def option_type(self):
        if self.optiontype == 1 and self.parent_id:
            return self.parent.option_type()
        else :
            return self.optiontype

    def __str__(self):
        return self.name

    def paths(self):
        return self.get_ancestors(ascending=False, include_self=True)

    def path_ids(self):
        return self.paths().values('id')

    def allproducts(self):
        from .Product import Product
        allcagetory_ids = self.get_descendants(include_self=True).values('id')
        return Product.objects.filter(cagetory__id__in=allcagetory_ids)

    # def parent_tags(self):
    #     parents = self.get_ancestors(ascending=False, include_self=False)
    #     tags = Tag.objects.usage_for_queryset(parents)
    #     return tags
    
    def allspecific(self):
        from .Specific import Specific
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