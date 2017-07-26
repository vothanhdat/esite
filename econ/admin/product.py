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


class ProSpecificDetailInline(SpecificDetailInline):
  verbose_name = "Specific"
  verbose_name_plural = "Specific"


class ProductForm(forms.ModelForm):
  class Media:
    js = ('product-admin.js',)
  class Meta:
    fields = ('__all__')
    widgets = {
      'product_cagetory' : AutoCompleteWiget('econ:cagetory-ac'),
    }


class NestedProductOptionInline(NestedStackedInline):
  model = ProductOption
  inlines=[OptionSpecificDetailInline]
  classes=('productoption-inline',)
  extra = 1


@admin.register(Product)
class ProductAdmin(NestedModelAdmin):

  form = ProductForm
  inlines = [ProSpecificDetailInline,ProductInfoInline,ProductImageInLine,NestedProductOptionInline,ProductPromotionInLine]
  list_display = ['product_name', 'product_cagetory', 'product_branch','product_price','product_quatity' ] 
  list_filter = [ ('product_cagetory', CustomTreeRelatedFieldListFilter),'product_branch','product_agency']
  search_fields = ['product_name', 'product_cagetory__cagetory_name', 'product_branch__brand_name' ] 

  formfield_overrides = {
    TagField: {'widget': AutoTaggingWiget('econ:tag-ac')},
  }

  fieldsets = (
    (None, {
        'fields': ('product_name', 'product_cagetory', 'product_branch','product_agency', 'product_price','product_quatity')
    }),
    ('Tagged', {
        'fields': ('tags', 'slug'),
    }),
  )

