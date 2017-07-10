from django.contrib import admin
from django import forms
from django.contrib.admin.sites import site
from django_mptt_admin.admin import DjangoMpttAdmin
from mptt.admin import TreeRelatedFieldListFilter,TreeNodeChoiceField

from .models import Brand,Cagetory,Product,ProductImage,BaseUser,Agency,AgencyMember,AgencyPromotion,ProductPromotion,Specific,SpecificDetail,ProductSpecDetail
from dal import autocomplete, forward



    

class MyModelAdmin(admin.ModelAdmin):
  def get_model_perms(self, request):
    return {}


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

class SpecificDetailForm(forms.ModelForm):

  class Meta:
    fields = ('__all__')

    widgets = {
      'specof' : AutoCompleteWiget(
        'econ:spec-ac',
        forward=['product_cagetory',forward.Field(src='productspecdetail_set---specof',dst='exist_id')],
        
      ),
      'spec': AutoCompleteWiget(
        'econ:prodspecdeit-ac',
        forward=['specof']
      ),
    }



class PostProduct(admin.ModelAdmin):
  # fields = ['name', 'by_admin']
  
  class ProductImageInLine(admin.TabularInline):
    model = ProductImage
    fields = ['image','image_link']
    extra = 1

  class ProductPromotionInLine(admin.StackedInline):
    model = ProductPromotion.apply_to.through
    extra = 1


  class SpecificDetailInline(admin.TabularInline):
    class SpecificDetailForm(forms.ModelForm):

      class Meta:
        fields = ('__all__')

        widgets = {
          'specof' : AutoCompleteWiget(
            'econ:spec-ac',
            forward=['product_cagetory',forward.Field(src='productspecdetail_set---specof',dst='exist_id')],
            
          ),
          'spec': AutoCompleteWiget(
            'econ:prodspecdeit-ac',
            forward=['specof']
          ),
        }

    model = ProductSpecDetail
    form = SpecificDetailForm


  class ProductForm(forms.ModelForm):
    class Meta:
      fields = ('__all__')
      widgets = {
        'product_cagetory' : AutoCompleteWiget('econ:cagetory-ac'),
      }

  form = ProductForm
  inlines = [SpecificDetailInline,ProductImageInLine,ProductPromotionInLine]
  list_display = ['product_name', 'product_cagetory', 'product_branch','product_price','product_quatity' ] 
  list_filter = [ ('product_cagetory', TreeRelatedFieldListFilter),'product_branch','product_agency']
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
  class SpecificDetailInline(admin.StackedInline):
    model = SpecificDetail
  inlines=[SpecificDetailInline]    

admin.site.register(Brand)
admin.site.register(Cagetory,CagetoryAdmin)
admin.site.register(BaseUser,BaseUserAdmin)
admin.site.register(Product,PostProduct)
admin.site.register(Specific,SpecificAdmin)
admin.site.register(SpecificDetail,MyModelAdmin)
admin.site.register(ProductPromotion)
admin.site.register(Agency,AgencyAdmin)