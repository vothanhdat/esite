from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views import generic
from ..models import TaggedInfo, Cagetory,Product,Brand

from .index import (
    indexbycagetory as cagetoryview,
    indexbybrand as brandview
)
from .product import index as productview
from django.http import Http404


def index(request,slug):
    try:
        slug = TaggedInfo.objects.get(slug=slug)
        content_object = slug.content_object
        if isinstance(content_object, Cagetory):
            return cagetoryview(request,slug.object_id,object=content_object)
        elif isinstance(content_object, Product):
            return productview(request,slug.object_id,object=content_object)
        elif isinstance(content_object, Brand):
            return brandview(request,slug.object_id,object=content_object)
        else:
            raise Http404("No MyModel matches the given query.")
    except:
        raise Http404("No MyModel matches the given query.")




