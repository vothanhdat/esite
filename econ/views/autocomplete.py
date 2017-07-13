from dal import autocomplete
from django.conf.urls import url

from ..models import SpecificDetail,Specific,Cagetory,Product




def loginRequired(original_class):
    origin_get_queryset = original_class.get_queryset
    origin_create_object = original_class.create_object

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return []
        else:
            return origin_get_queryset(self)

    def create_object(self,text):
        if not self.request.user.is_authenticated():
            return []
        else:
            return origin_create_object(self,text)


    original_class.get_queryset = get_queryset 
    original_class.create_object = create_object 

    return original_class



@loginRequired
class SpecificDetailAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = SpecificDetail.objects.all()
        specof = self.forwarded.get('specof', None)
        if specof:
            qs = qs.filter(detail_field__id=specof)
        else :
            return Specific.objects.none()

        if self.q:
            qs = qs.filter(detail_value__istartswith=self.q)

        return qs

    def create_object(self, text):
        specific = self.forwarded.get('specof', None)
        return self.get_queryset().create(**{
            self.create_field: text,
            'detail_field_id':specific
        })

@loginRequired
class SpecificAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        
        qs = Specific.objects.all()
        specific_of = self.forwarded.get('product_cagetory', None)
        prod_id = self.forwarded.get('prod', None)

        if specific_of:
            cagetory = Cagetory.objects.get(id=specific_of)
            qs = cagetory.allspecific()
        elif prod_id:
            prod = Product.objects.get(id=prod_id)
            specific_ids = prod.productspecdetail_set.values("specof__id")
            qs = qs.filter(id__in=specific_ids)
        else :
            return Specific.objects.none()
            
            
        if self.q:
            qs = qs.filter(specific_name__istartswith=self.q)

        return qs

    def create_object(self, text):
        specific_of = self.forwarded.get('product_cagetory', None)
        return self.get_queryset().create(**{
            self.create_field: text,
            'specific_of_id':specific_of,
        })



@loginRequired
class CagetoryAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Cagetory.objects.all()
        if self.q:
            qs = qs.filter(cagetory_name__istartswith=self.q)
        return qs



app_name = 'econ'
urlpatterns = [
    url(
        r'^specific/$',
        SpecificAutoComplete.as_view(
            create_field='specific_name',
            model=Specific),
        name='spec-ac'
    ),
    url(
        r'^specificdetail/$',
        SpecificDetailAutoComplete.as_view(
            create_field='detail_value',
            model=SpecificDetail),
        name='prodspecdeit-ac'
    ),
    url(
        r'^cagetory/$',
        CagetoryAutoComplete.as_view(),
        name='cagetory-ac'
    ),
]
