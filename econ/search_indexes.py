import datetime
from haystack import indexes
from .models import Product, Cagetory, Brand


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.NgramField(model_attr='name')
    tags = indexes.NgramField(model_attr='tags')
    lastupdate = indexes.DateTimeField(model_attr='modified')


    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return Product.objects.none()


class CagetoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.NgramField(model_attr='cagetory_name')
    tags = indexes.NgramField(model_attr='tags')
    lastupdate = indexes.DateTimeField(model_attr='modified')

    def get_model(self):
        return Cagetory

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return Cagetory.objects.none()


class BrandIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.NgramField(model_attr='brand_name')
    tags = indexes.NgramField(model_attr='tags')
    lastupdate = indexes.DateTimeField(model_attr='modified')

    def get_model(self):
        return Brand

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return Brand.objects.none()


