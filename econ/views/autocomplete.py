from dal import autocomplete

from ..models import SpecificDetail


class SpecificDetailAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = SpecificDetail.objects.all()

        if self.q:
            qs = qs.filter(detail_field__specific_name__istartswith=self.q)

        return qs