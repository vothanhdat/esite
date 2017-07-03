from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views import generic
from ..models import Brand,Cagetory,Product,ProductImage,BaseUser,Agency,AgencyMember,AgencyPromotion,ProductPromotion,ProductSpecific,ProductSpecificDetail


# class ProductListView(generic.ListView):
#     template = loader.get_template('list_product.html')
    
# Create your views here.
def index(request):
    product_list = Product.objects.all()[:5]
    print product_list
    template = loader.get_template('list_product.html')
    context = {
        'product_list': product_list,
    }
    return HttpResponse(template.render(context, request))