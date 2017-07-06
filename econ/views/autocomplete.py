from dal import autocomplete
from django.conf.urls import url
from ..models import SpecificDetail,Specific


class SpecificDetailAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = SpecificDetail.objects.all()

        if self.q:
            qs = qs.filter(detail_field__specific_name__istartswith=self.q)

        return qs

class SpecificAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Specific.objects.all()

        if self.q:
            qs = qs.filter(specific_name__istartswith=self.q)

        return qs


app_name = 'econ'
urlpatterns = [
    url(r'^spec_auco/$',SpecificAutoComplete.as_view(),name='specac'),
    url(r'^prodspecdeit_auco/$',SpecificDetailAutoComplete.as_view(),name='prodspecdeitac'),
]
