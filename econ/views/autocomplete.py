from dal import autocomplete
from django.conf.urls import url
from ..models import SpecificDetail,Specific,Cagetory


class SpecificDetailAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = SpecificDetail.objects.all()
        specof = self.forwarded.get('specof', None)
        if specof:
            qs = qs.filter(detail_field__id=specof)
        if self.q:
            qs = qs.filter(detail_value__istartswith=self.q)

        return qs

    def create_object(self, text):
        specific = self.forwarded.get('specof', None)
        return self.get_queryset().create(**{
            self.create_field: text,
            'detail_field_id':specific
        })


class SpecificAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        
        qs = Specific.objects.all()
        specific_of = self.forwarded.get('product_cagetory', None)

        if specific_of:
            cagetory = Cagetory.objects.get(id=specific_of)
            qs = cagetory.allspecific()
            
        if self.q:
            qs = qs.filter(specific_name__istartswith=self.q)

        return qs

    
    def create_object(self, text):
        specific_of = self.forwarded.get('product_cagetory', None)
        return self.get_queryset().create(**{
            self.create_field: text,
            'specific_of_id':specific_of
        })



app_name = 'econ'
urlpatterns = [
    url(
        r'^spec_auco/$',
        SpecificAutoComplete.as_view(
            create_field='specific_name',
            model=Specific),
        name='spec-ac'
    ),
    url(
        r'^prodspecdeit_auco/$',
        SpecificDetailAutoComplete.as_view(
            create_field='detail_value',
            model=SpecificDetail),
        name='prodspecdeit-ac'
    ),
]
