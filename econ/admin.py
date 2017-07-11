from django.contrib import admin
from django import forms
from django.contrib.admin.sites import site
from django_mptt_admin.admin import DjangoMpttAdmin
from mptt.admin import TreeRelatedFieldListFilter,TreeNodeChoiceField

from .models import Brand,Cagetory,Product,ProductImage,BaseUser,Agency,AgencyMember,AgencyPromotion,ProductPromotion,Specific,SpecificDetail,ProductSpecDetail
from dal import autocomplete, forward

from django.utils.translation import ugettext as _, ugettext_lazy
from django.utils.encoding import smart_text
from django.db.models.fields.related import ForeignObjectRel, ManyToManyField
from mptt.compat import remote_field, remote_model
from django.utils.translation import get_language_bidi
from django.utils.html import format_html, mark_safe


    

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


class CustomTreeRelatedFieldListFilter(TreeRelatedFieldListFilter):
  template='custom_mptt_filter.html'
  
  class Media:
    css = {
      'all': (
        'scss/custom_mptt_filter.scss',
      )
    }

  def field_choices(self, field, request, model_admin):

    return field.related_model._default_manager.filter(level__lte=0)

  def choice_recuser(self,lookup_choices, cl,EMPTY_CHANGELIST_VALUE):
    for model in lookup_choices:
      yield {
        'query_string': cl.get_query_string({
          self.changed_lookup_kwarg: model.id,
        }, [self.lookup_kwarg_isnull]),
        'display': model,
        'child': self.choice_recuser(
          model.get_children().all(),
          cl,
          EMPTY_CHANGELIST_VALUE
        ) if model.get_descendant_count() else None,
      }


  def choices(self, cl):
    # #### MPTT ADDITION START
    try:
      # EMPTY_CHANGELIST_VALUE has been removed in django 1.9
      from django.contrib.admin.views.main import EMPTY_CHANGELIST_VALUE
    except:
      EMPTY_CHANGELIST_VALUE = self.empty_value_display
    # #### MPTT ADDITION END
    yield {
      'selected': self.lookup_val is None and not self.lookup_val_isnull,
      'query_string': cl.get_query_string({
        self.changed_lookup_kwarg: None,
      }, [self.lookup_kwarg, self.lookup_kwarg_isnull]),
      'display': _('All'),
    }
    for choice in self.choice_recuser(self.lookup_choices,cl,EMPTY_CHANGELIST_VALUE):
      yield choice


    # for model in self.lookup_choices:
    #   print model
    #   yield {
    #     'query_string': cl.get_query_string({
    #       self.changed_lookup_kwarg: model.id,
    #     }, [self.lookup_kwarg_isnull]),
    #     'display': model,
    #     'child': model,
    #   }
    # if (isinstance(self.field, ForeignObjectRel) and
    #     (self.field.field.null or isinstance(self.field.field, ManyToManyField)) or
    #     remote_field(self.field) is not None and
    #     (self.field.null or isinstance(self.field, ManyToManyField))):
    #   yield {
    #     'selected': bool(self.lookup_val_isnull),
    #     'query_string': cl.get_query_string({
    #       self.lookup_kwarg_isnull: 'True',
    #     }, [self.lookup_kwarg]),
    #     'display': EMPTY_CHANGELIST_VALUE,
    #   }




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