
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from .BaseUser import BaseUser
from .Slug import Slug

class Agency(models.Model):
    name = models.CharField(max_length=100,null=True, blank=True)
    logo = models.ImageField(upload_to='media/%Y/%m/%d/%H/%M/%S/',null=True, blank=True)
    member = models.ManyToManyField(
        BaseUser,
        through='AgencyMember',
        through_fields=('agency', 'user'),
    )
    slug = GenericRelation(Slug)
    def __str__(self):
        return self.name
