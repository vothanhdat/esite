from django.contrib import admin
from django import forms
from django.contrib.admin.sites import site
from django_mptt_admin.admin import DjangoMpttAdmin
from mptt.admin import TreeRelatedFieldListFilter,TreeNodeChoiceField

from .models import Brand,Cagetory,Product,ProductImage,BaseUser,Agency,AgencyMember
from .models import AgencyPromotion,ProductPromotion,Specific,SpecificDetail,ProductSpecDetail
from .models import ProductOption,ProductImage
from dal import autocomplete, forward
from .admin_customtreefilter import CustomTreeRelatedFieldListFilter

from django.utils.html import format_html_join,format_html
from django.utils.safestring import mark_safe    

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
  autocomplete_function = 'select2'
  class Media:
    js = (
        'custom.js',
    )
    css = {
      'all': (
        'custom.css',
      )
    }





class SpecificDetailInline(admin.TabularInline):
  class SpecificDetailForm(forms.ModelForm):
    
    class Meta:
      fields = ('specof','spec','desc')
      
      widgets = {
        'specof' : AutoCompleteWiget(
          'econ:spec-ac',
          forward=[
            'product_cagetory',
            'prod',
            Exclude(exclude='productspecdetail_set---specof')
          ],
          
        ),
        'spec': AutoCompleteWiget(
          'econ:prodspecdeit-ac',
          forward=['specof']
        ),
      }

  model = ProductSpecDetail
  form = SpecificDetailForm


class PostProduct(admin.ModelAdmin):
  # fields = ['name', 'by_admin']
  
  class ProductImageInLine(admin.TabularInline):
    model = ProductImage
    fields = ['image','image_link']
    extra = 1

  class ProductPromotionInLine(admin.StackedInline):
    model = ProductPromotion.apply_to.through
    extra = 1


  class ProductOptionInline(admin.StackedInline):
    # template = "custom_product_option.html"
    show_change_link = True
    model = ProductOption
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
  list_filter = [ ('specific_of', TreeRelatedFieldListFilter)]
  


class ProductOptionAdmin(admin.ModelAdmin):
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

admin.site.register(Brand)
admin.site.register(Cagetory,CagetoryAdmin)
admin.site.register(BaseUser,BaseUserAdmin)
admin.site.register(Product,PostProduct)
admin.site.register(Specific,SpecificAdmin)
admin.site.register(SpecificDetail,MyModelAdmin)
admin.site.register(ProductPromotion)
admin.site.register(Agency,AgencyAdmin)
admin.site.register(ProductOption,ProductOptionAdmin)