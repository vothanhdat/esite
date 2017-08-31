from django.contrib import admin
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.utils.html import format_html

from util.func import rabdombase64,addparamtourl
from util.wiget.autocomplete import AutoCompleteWiget
from econ.models import Product, ProductOption, ProductImage, ProductPromotion, ProductSpecDetail, ProductInfo
from util.admin.admin_custommodelpopup import RANDOM_VAR
from util.admin.admin_customtreefilter import CustomTreeRelatedFieldListFilter

from .specificdetail  import SpecificDetailInline, OptionSpecificDetailInline
from django import forms
from tagging.fields import TagField
from util.wiget.autocomplete import AutoTaggingWiget
from django.utils.html import format_html_join
from nested_admin.nested import NestedModelAdmin,NestedInlineModelAdmin,NestedStackedInline,NestedTabularInline
from .slug  import SlugFieldFormMixin


__all__= ()

class ProductImageInLine(NestedTabularInline):
  verbose_name = "Photos"
  verbose_name_plural = "Photos"
  model = ProductImage
  fields = ['image','link']
  extra = 1

class ProductPromotionInLine(NestedStackedInline):
  model = ProductPromotion.apply_to.through
  extra = 1
  verbose_name = "Promotions"
  verbose_name_plural = "Promotions"

class ProductInfoInline(NestedStackedInline):
  model = ProductInfo
  verbose_name = "Detail"
  verbose_name_plural = "Detail"
  can_delete = False
  is_sortable = False


class ProSpecificDetailInline(SpecificDetailInline):
  verbose_name = "Specific"
  verbose_name_plural = "Specific"


class ProductForm(SlugFieldFormMixin, forms.ModelForm):
  class Media:
    js = ('product-admin.js',)
  class Meta:
    fields = ('__all__')
    widgets = {
      'cagetory' : AutoCompleteWiget('econ:cagetory-ac'),
      'tags' : AutoTaggingWiget('econ:tag-ac'),
    }


class NestedProductOptionInline(NestedStackedInline):
  model = ProductOption
  inlines=[OptionSpecificDetailInline]
  classes=('productoption-inline',)
  extra = 1
  is_sortable = False
  fields = (
    ('quatity', 'price', ),
  )

@admin.register(Product)
class ProductAdmin(NestedModelAdmin):

  form = ProductForm
  inlines = [ProSpecificDetailInline,ProductInfoInline,ProductImageInLine,NestedProductOptionInline,ProductPromotionInLine]
  list_display = ['name','slug_field','isvariety', 'cagetory', 'branch','price','quatity' ] 
  list_filter = [ ('cagetory', CustomTreeRelatedFieldListFilter),'isvariety', 'branch',]
  search_fields = ['name', 'cagetory__name', 'branch__name' ] 
 
  fieldsets = (
    (None, {
        'fields': ('name', 'cagetory', 'branch', 'price','quatity','isvariety')
    }),
    ('Tagged', {
        'fields': ('tags', 'slug_field'),
    }),
  )

  def save_related(self, request, form, formsets, change):
    r = super(ProductAdmin,self).save_related(request, form, formsets, change)
    
    if hasattr(form,'save_related') and callable(form.save_related):
      form.save_related(request, form, formsets, change)
    return r

  def get_queryset(self, request):
    qs = super(ProductAdmin, self).get_queryset(request)
    return qs.prefetch_related(
      'slug'
    ) .select_related(
      'cagetory',
      'branch',
    )
