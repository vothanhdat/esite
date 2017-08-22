import datetime
from haystack import indexes
from .models import Product, Cagetory, Brand


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.NgramField(model_attr='product_name')

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return Product.objects.all()


class CagetoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.NgramField(model_attr='cagetory_name')

    def get_model(self):
        return Cagetory

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return Cagetory.objects.all()


class BrandIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.NgramField(model_attr='brand_name')

    def get_model(self):
        return Brand

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return Brand.objects.all()


