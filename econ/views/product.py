from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views import generic
from ..models import Brand,Cagetory,Product,ProductImage,BaseUser,Agency,AgencyMember,AgencyPromotion,ProductPromotion,Specific,SpecificDetail
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

# class ProductListView(generic.ListView):
#     template = loader.get_template('list_product.html')
    
# Create your views here.
# @login_required
# @cache_page(60 * 15)
def index(request,product_id,object=None):

    product = object or Product.objects.get(id=product_id)

    product_details = product.productspecdetail_set.prefetch_related(
        'spec',
        'spec__detail_field'
    )

    template = loader.get_template('product-detail.html')
    context = {
        'product': product,
        'product_details': product_details
    }
    
    return HttpResponse(template.render(context, request))