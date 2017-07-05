from dal import autocomplete

from ..models import ProductSpecificDetail


class ProductSpecificDetailAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = ProductSpecificDetail.objects.all()

        if self.q:
            qs = qs.filter(detail_field__specific_name__istartswith=self.q)

        return qs