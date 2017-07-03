from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views import generic
from ..models import Brand,Cagetory,Product,ProductImage,BaseUser,Agency,AgencyMember,AgencyPromotion,ProductPromotion,ProductSpecific,ProductSpecificDetail
import itertools


# class ProductListView(generic.ListView):
#     template = loader.get_template('list_product.html')
    
# Create your views here.
def index(request):
    product_list = Product.objects.all()[:5]
    cagetory_list = Cagetory.objects.filter(cagetory_parent=None)
    template = loader.get_template('list_product.html')
    context = {
        'product_list': product_list,
        'cagetory_list': cagetory_list
    }
    return HttpResponse(template.render(context, request))

def indexbycagetory(request,cagetory_id):
    cagetoty = Cagetory.objects.get(id=cagetory_id)
    cagetory_list = Cagetory.objects.filter(cagetory_parent__id=cagetory_id)[:5]
    product_list = list(itertools.islice(cagetoty.allproducts(),5))
    print product_list
    template = loader.get_template('list_product.html')
    context = {
        'product_list': product_list,
        'cagetory_list': cagetory_list,
    }
    return HttpResponse(template.render(context, request))