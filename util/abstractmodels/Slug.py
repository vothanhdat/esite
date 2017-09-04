from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


class Slug(models.Model):
    class Meta:
        app_label = 'econ'
        
    slug = models.SlugField(unique=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self): 
        return self.slug
    

class SlugMixin(models.Model):
    class Meta:
         abstract = True

    slug = GenericRelation(Slug)
  
    @property
    def slug_field(self):
        list_slug = self.slug.all()
        return list_slug[0] if list_slug.count() > 0 else None