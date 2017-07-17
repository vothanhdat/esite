from django.contrib import admin
from django import forms
from django.contrib.admin.sites import site
from django_mptt_admin.admin import DjangoMpttAdmin
from mptt.admin import TreeRelatedFieldListFilter,TreeNodeChoiceField

from .models import Brand,Cagetory,Product,ProductImage,BaseUser,Agency,AgencyMember
from .models import AgencyPromotion,ProductPromotion,Specific,SpecificDetail,ProductSpecDetail
from .models import ProductOption,ProductImage
from dal import autocomplete, forward

from django.utils.html import format_html_join,format_html
from django.utils.safestring import mark_safe    


from django.template.response import TemplateResponse, SimpleTemplateResponse
from django.template.loader import render_to_string


from util.admin.admin_customtreefilter import CustomTreeRelatedFieldListFilter, InheritTreeRelatedFieldListFilter
from util.admin.admin_custommodelpopup import CustomAdminPopup



IS_POPUP_VAR = '_popup'
RANDOM_VAR = '_random'

# import nested_admin
from django.core.urlresolvers import reverse
try:
    import urlparse
    from urllib import urlencode
except: # For Python 3
    import urllib.parse as urlparse
    from urllib.parse import urlencode


import uuid
import base64
def rabdombase64():
  return base64.b64encode(uuid.uuid4().bytes).replace('=', '')

def addparamtourl(url,params):
  url_parts = list(urlparse.urlparse(url))
  query = dict(urlparse.parse_qsl(url_parts[4]))
  query.update(params)
  url_parts[4] = urlencode(query)
  return urlparse.urlunparse(url_parts)

class MyModelAdmin(admin.ModelAdmin):
  def get_model_perms(self, request):
    return {}


class Exclude(forward.Forward):
    type = "exclude"
    def __init__(self, exclude):
        self.exclude = exclude
    def to_dict(self):
        d = super(Exclude, self).to_dict()
        d.update(exclude=self.exclude)
        return d

class AutoCompleteWiget(autocomplete.ModelSelect2):
  autocomplete_function = 'customselect2'
  class Media:
    js = (
        'custom.js',
    )
    css = {
      'all': (
        'custom.css',
      )
    }


class SpecificDetailForm(forms.ModelForm):
  class Meta:
    fields = ('specof','spec','desc')

  specofwidget = AutoCompleteWiget(
    'econ:spec-ac',
    forward=[
      'product_cagetory',
      'prod',
      Exclude(exclude='productspecdetail_set---specof')
    ],
  )
  specwiget = AutoCompleteWiget(
    'econ:prodspecdeit-ac',
    forward=['specof']
  )

  specof = forms.ModelChoiceField(queryset=Specific.objects.all(),widget = specofwidget)
  spec = forms.ModelChoiceField(queryset=SpecificDetail.objects.all(),widget = specwiget)

  def get_initial_for_field(self,field, field_name):
    instance = self.instance
    if instance and field_name == 'specof' and instance.spec_id:
      return instance.spec.detail_field
    else:
      return super(SpecificDetailForm,self).get_initial_for_field(field, field_name)
      




class SpecificDetailInline(admin.TabularInline):
  model = ProductSpecDetail
  form = SpecificDetailForm
  extra = 1


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

class PostProduct(admin.ModelAdmin):
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

class BaseUserAdmin(admin.ModelAdmin):
  class BaseUserMemberInline(admin.StackedInline):
    model = AgencyMember
    fk_name = 'user'
    exclude = ('inviter',)
  inlines = [BaseUserMemberInline]
  extra = 1

class AgencyAdmin(admin.ModelAdmin):
  class AgencyMembersInline(admin.StackedInline):
    model = AgencyMember
    fk_name = 'agency'
    exclude = ('inviter',)
    extra = 1
  class AgencyPromotionsInline(admin.StackedInline):
    model = AgencyPromotion
    fk_name = 'apply_to'
    extra = 1
    
  inlines = [AgencyMembersInline,AgencyPromotionsInline]

class CagetoryAdmin(DjangoMpttAdmin):

  tree_auto_open = False

class SpecificAdmin(admin.ModelAdmin):
  list_display = ['specific_name', 'specific_of'] 
  list_filter = [ ('specific_of', InheritTreeRelatedFieldListFilter)]
  


class ProductOptionAdmin(CustomAdminPopup):
  popup_response_template = "product_specific_detail.html"
  inlines = [SpecificDetailInline]
  readonly_fields = ('product',)
  fields = ('product','product_price',)

  def product(self, instance):
    try:
       return format_html('<input value="{}" name="prod" readonly style="display:none;"/><b>{}</b>',instance.prod.id,instance.prod)
    except:
      if self.prod_id:
        prod = Product.objects.get(id=self.prod_id)
        return format_html('<input value="{}" name="prod" readonly style="display:none;"/><b>{}</b>',prod.id,prod)

      return format_html('<input value="11" name="prod" readonly style="display:none;"/><b></b>')

  def get_changeform_initial_data(self, request):
    self.prod_id = request.GET.get('prod',None)
    return super(ProductOptionAdmin,self).get_changeform_initial_data(request)


  def save_form(self, request, form, change):
    prod_id = request.GET.get('prod',None)
    r = super(ProductOptionAdmin, self).save_form(request, form, change)
    if prod_id and not change:
      r.prod_id = prod_id
    return r

  def get_model_perms(self, request):
    return {}

  def get_popup_context(self,request,obj):
    return {'details' : obj.prod_details(),}

admin.site.register(Brand)
admin.site.register(Cagetory,CagetoryAdmin)
admin.site.register(BaseUser,BaseUserAdmin)
admin.site.register(Product,PostProduct)
admin.site.register(Specific,SpecificAdmin)
admin.site.register(SpecificDetail,MyModelAdmin)
admin.site.register(ProductPromotion)
admin.site.register(Agency,AgencyAdmin)
admin.site.register(ProductOption,ProductOptionAdmin)