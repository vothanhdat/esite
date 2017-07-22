from django.db.models import Prefetch
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views import generic
from ..models import Brand,Cagetory,Product,ProductImage,BaseUser,Agency,AgencyMember,AgencyPromotion,ProductPromotion,Specific,SpecificDetail

import itertools


# class ProductListView(generic.ListView):
#     template = loader.get_template('list_product.html')
    
# Create your views here.
def index(request):
    product_list = Product.objects.all().prefetch_related(
        Prefetch('productimage_set', to_attr='images'),
        'product_agency'
    )
    template = loader.get_template('list_product.html')
    context = {
        'product_list': product_list,
    }
    return HttpResponse(template.render(context, request))

def indexbycagetory(request,cagetory_id,object=None):
    page = request.GET.get('page') or 1
    cagetoty = object or Cagetory.objects.get(id=cagetory_id)
    product_list = cagetoty.allproducts().prefetch_related(
        Prefetch('productimage_set', to_attr='images'),
        'product_agency'
    )
    template = loader.get_template('list_product.html')
    context = {
        'cagetory_paths' : cagetoty.paths(),
        'product_list': product_list,
    }
    return HttpResponse(template.render(context, request))

def indexbybrand(request,brand_id,object=None):
    page = request.GET.get('page') or 1
    brand = object or Brand.objects.get(id=brand_id)
    product_list = brand.product_set.prefetch_related(
        Prefetch('productimage_set', to_attr='images'),
        'product_agency'
    )
    template = loader.get_template('list_product.html')
    context = {
        'product_list': product_list,
    }
    return HttpResponse(template.render(context, request))