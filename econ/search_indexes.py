import datetime
from haystack import indexes
from .models import Product, Cagetory, Brand


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return Product.objects.all()


class CagetoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Cagetory

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return Cagetory.objects.all()

print 'searchIndexRun'