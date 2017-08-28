from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from tagging.fields import TagField
from .ModifyLog import ModifyLog
from .Slug import Slug

class Brand(ModifyLog,models.Model):
    name = models.CharField(max_length=100)
    sym = models.CharField(max_length=20)
    logo = models.ImageField(upload_to='media/%Y/%m/%d/%H/%M/%S/',null=True, blank=True)
    tags = TagField()
    slug = GenericRelation(Slug)

    def __str__(self):
        return self.name
