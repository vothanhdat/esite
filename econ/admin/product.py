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
  fields = ['image','image_link']
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


@admin.register(Product)
class ProductAdmin(NestedModelAdmin):

  form = ProductForm
  inlines = [ProSpecificDetailInline,ProductInfoInline,ProductImageInLine,NestedProductOptionInline,ProductPromotionInLine]
  list_display = ['name','slug_field','cagetory', 'branch','price','quatity' ] 
  list_filter = [ ('cagetory', CustomTreeRelatedFieldListFilter),'branch','agency']
  search_fields = ['name', 'cagetory__cagetory_name', 'branch__brand_name' ] 
 
  fieldsets = (
    (None, {
        'fields': ('name', 'cagetory', 'branch','agency', 'price','quatity')
    }),
    ('Tagged', {
        'fields': ('tags', 'slug_field'),
    }),
  )

  def slug_field(self,instance):
    return instance.slug.first()


  def save_related(self, request, form, formsets, change):
    r = super(ProductAdmin,self).save_related(request, form, formsets, change)
    
    if hasattr(form,'save_related') and callable(form.save_related):
      form.save_related(request, form, formsets, change)
    return r
