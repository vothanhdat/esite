from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views import generic
from ..models import Brand,Cagetory,Product,ProductImage,BaseUser,Agency,AgencyMember,AgencyPromotion,ProductPromotion,ProductSpecific,ProductSpecificDetail


# class ProductListView(generic.ListView):
#     template = loader.get_template('list_product.html')
    
# Create your views here.
def index(request,product_id):
    product = Product.objects.get(id=product_id)
    print (product)
    template = loader.get_template('product_detail.html')
    context = {
        'product': product,
    }
    return HttpResponse(template.render(context, request))