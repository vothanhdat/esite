from django.contrib import admin
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.utils.html import format_html

from util.func import rabdombase64,addparamtourl
from util.wiget.autocomplete import AutoCompleteWiget
from econ.models import ProductOption, ProductImage, ProductPromotion, ProductSpecDetail
from util.admin.admin_custommodelpopup import RANDOM_VAR
from util.admin.admin_customtreefilter import CustomTreeRelatedFieldListFilter

from .specificdetail  import SpecificDetailInline
from django import forms
from ..models import Product



class ProductOptionInline(admin.StackedInline):
  template = "custom_product_option.html"
  model = ProductOption
  extra = 1
  readonly_fields = ('specific_detail',)
  fields = ('specific_detail', )
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
        'product_specific_detail.html',
        {'details' : self.prod_details(instance),}
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
    return instance.productspecdetail_set.all()[:]


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
    model = ProductImage
    fields = ['image','image_link']
    extra = 1

  class ProductPromotionInLine(admin.StackedInline):
    model = ProductPromotion.apply_to.through
    extra = 1


  class ProductForm(forms.ModelForm):
    class Meta:
      fields = ('__all__')
      widgets = {
        'product_cagetory' : AutoCompleteWiget('econ:cagetory-ac'),
      }

  form = ProductForm
  inlines = [SpecificDetailInline,ProductImageInLine,ProductOptionInline,ProductPromotionInLine]
  list_display = ['product_name', 'product_cagetory', 'product_branch','product_price','product_quatity' ] 
  list_filter = [ ('product_cagetory', CustomTreeRelatedFieldListFilter),'product_branch','product_agency']
  search_fields = ['product_name', 'product_cagetory__cagetory_name', 'product_branch__brand_name' ] 
