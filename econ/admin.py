from django.contrib import admin
from django import forms
from django.contrib.admin.sites import site
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import Brand,Cagetory,Product,ProductImage,BaseUser,Agency,AgencyMember,AgencyPromotion,ProductPromotion,Specific,SpecificDetail,ProductSpecDetail
from dal import autocomplete, forward



    

class MyModelAdmin(admin.ModelAdmin):
  def get_model_perms(self, request):
    return {}


class SpecificDetailForm(forms.ModelForm):

  class Meta:
    fields = ('__all__')

    widgets = {
      'specof' : autocomplete.ModelSelect2(
        'econ:spec-ac',
        forward=['product_cagetory','productspecdetail_set-0-specof','productspecdetail_set-1-specof','productspecdetail_set-2-specof','productspecdetail_set-3-specof','productspecdetail_set-4-specof']
      ),
      'spec': autocomplete.ModelSelect2(
        'econ:prodspecdeit-ac',
        forward=['specof']
      ),
    }


class PostProduct(admin.ModelAdmin):
  # fields = ['name', 'by_admin']
  
  class ProductImageInLine(admin.StackedInline):
    model = ProductImage
    fields = ['image']
    extra = 1

  class ProductPromotionInLine(admin.StackedInline):
    model = ProductPromotion.apply_to.through
    extra = 1


  class SpecificDetailInline(admin.TabularInline):
    model = ProductSpecDetail
    form = SpecificDetailForm


  inlines = [SpecificDetailInline,ProductImageInLine,ProductPromotionInLine]


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


  class ProductInline(admin.TabularInline):
    model = Product

    class ProductImageInLine(admin.StackedInline):
      model = ProductImage
      fields = ['image']
      extra = 1
    inlines = [ProductImageInLine]
    extra = 1
    
  tree_auto_open = False
  inlines = [ProductInline]

admin.site.register(Brand)
admin.site.register(Cagetory,CagetoryAdmin)
admin.site.register(BaseUser,BaseUserAdmin)
admin.site.register(Product,PostProduct)
admin.site.register(Specific)
admin.site.register(SpecificDetail)
admin.site.register(ProductPromotion)
admin.site.register(Agency,AgencyAdmin)