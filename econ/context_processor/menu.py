from django.core.cache import cache

from ..models import Brand,Cagetory,Product,ProductImage,Customer,Agency,AgencyMember,AgencyPromotion,ProductPromotion,Specific,SpecificDetail



def cagetory_list(request):
    cagetory_list_hash = Cagetory.hash()
    cagetory_list = Cagetory.objects.all()
    return {
        'cagetory_list': cagetory_list,
        'cagetory_list_hash' : cagetory_list_hash,
    }



def index(request):
    return {}