from django.contrib import admin
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.utils.html import format_html

from util.func import rabdombase64,addparamtourl
from util.wiget.autocomplete import AutoCompleteWiget
from econ.models import ProductOption, ProductImage, ProductPromotion, ProductSpecDetail, ProductInfo
from util.admin.admin_custommodelpopup import RANDOM_VAR
from util.admin.admin_customtreefilter import CustomTreeRelatedFieldListFilter

from .specificdetail  import SpecificDetailInline
from django import forms
from ..models import Product



class ProductOptionInline(admin.StackedInline):
  template = "compact_admin_inline.html"
  model = ProductOption
  extra = 1
  readonly_fields = ('specific_detail',)
  fields = ('specific_detail', )
  can_delete = True
  verbose_name = "Options"
  verbose_name_plural = "Options"

  def specific_detail(self, instance):
    reference_url = ''
    render_content = 'Click to Add'
    random = rabdombase64()
    params = {
      "_popup": True,
      RANDOM_VAR : random,
    }
    if instance.id:
      reference_url = reverse( 'admin:econ_productoption_change', args=(instance.id,)  )
      render_content = render_to_string(
        'product_option_compact.html',
        { 'product' : instance }
      ) 
    else : 
      reference_url = reverse('admin:econ_productoption_add')
      if self.parent_obj:
        params['prod'] = self.parent_obj.id


    return format_html(
      '<a href="{}" target="_blank" id="{}" class="related-widget-wrapper-link add-related">{}</a>',
      addparamtourl(reference_url,params) ,
      random  ,
      render_content
    )


  def prod_details(self,instance):
    return instance.prod_details()


  def get_formset(self, request, obj=None, **kwargs):
    self.parent_obj = obj
    return super(ProductOptionInline, self).get_formset(request, obj, **kwargs)

  specific_detail.allow_tags = True
  can_delete = True
  show_change_link = True




@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  # fields = ['name', 'by_admin']
  
  class ProductImageInLine(admin.TabularInline):
    verbose_name = "Photos"
    verbose_name_plural = "Photos"
    model = ProductImage
    fields = ['image','image_link']
    extra = 1

  class ProductPromotionInLine(admin.StackedInline):
    model = ProductPromotion.apply_to.through
    extra = 1
    verbose_name = "Promotions"
    verbose_name_plural = "Promotions"

  class ProductInfoInline(admin.StackedInline):
    model = ProductInfo
    verbose_name = "Detail"
    verbose_name_plural = "Detail"

  class ProSpecificDetailInline(SpecificDetailInline):
    verbose_name = "Specific"
    verbose_name_plural = "Specific"


  class ProductForm(forms.ModelForm):
    class Media:
      js = (
        'product-admin.js',
      )
    class Meta:
      fields = ('__all__')
      widgets = {
        'product_cagetory' : AutoCompleteWiget('econ:cagetory-ac'),
      }

  form = ProductForm
  inlines = [ProSpecificDetailInline,ProductInfoInline,ProductImageInLine,ProductOptionInline,ProductPromotionInLine]
  list_display = ['product_name', 'product_cagetory', 'product_branch','product_price','product_quatity' ] 
  list_filter = [ ('product_cagetory', CustomTreeRelatedFieldListFilter),'product_branch','product_agency']
  search_fields = ['product_name', 'product_cagetory__cagetory_name', 'product_branch__brand_name' ] 
