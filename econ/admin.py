from django.contrib import admin
from django import forms
from django.contrib.admin.sites import site
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import Brand,Cagetory,Product,ProductImage,BaseUser,Agency,AgencyMember,AgencyPromotion,ProductPromotion,ProductSpecific,ProductSpecificDetail
from dal import autocomplete



# <select name="{{ widget.name }}"{% include "django/forms/widgets/attrs.html" %}>{% for group_name, group_choices, group_index in widget.optgroups %}{% if group_name %}
#   <optgroup label="{{ group_name }}">{% endif %}{% for option in group_choices %}
#   {% include option.template_name with widget=option %}{% endfor %}{% if group_name %}
#   </optgroup>{% endif %}{% endfor %}
# </select>
#<option value="{{ widget.value }}"{% include "django/forms/widgets/attrs.html" %}>{{ widget.label }}</option>


# class ProductSpecWrapper(admin.widgets.RelatedFieldWidgetWrapper):
#   template_name = 'custom_related_widget_wrapper.html'

#   def get_context(self, name, value, attrs):
#     context = super(ProductSpecWrapper, self).get_context(name, value, attrs)
#     print (value)
#     return context



    

class MyModelAdmin(admin.ModelAdmin):
  def get_model_perms(self, request):
    return {}


class PostProduct(admin.ModelAdmin):
  # fields = ['name', 'by_admin']
  
  class ProductImageInLine(admin.StackedInline):
    model = ProductImage
    fields = ['image']
    extra = 1

  class ProductPromotionInLine(admin.StackedInline):
    model = ProductPromotion.apply_to.through
    extra = 1
    
  class ProductAdminForm(forms.ModelForm):
    class Media:
      js = ('custom.js',)
    class Meta:
      # model = Product
      fields = ('__all__')
      # product_detail = forms.ModelMultipleChoiceField(
      #   queryset=ProductSpecificDetail.objects.all(),
      #   widget=autocomplete.ModelSelect2Multiple(url='econ:prodspecdeitac')
      # )
      widgets = {
        'product_detail': autocomplete.ModelSelect2Multiple('econ:prodspecdeitac'),
      }

  # def get_form(self, request, obj=None, **kwargs):
  #   self.parent_obj = obj
  #   print (super(PostProduct, self))
  #   return super(PostProduct, self).get_form(request, obj, **kwargs)


  # def formfield_for_manytomany(self, db_field, request, **kwargs):
  #   if db_field.name == "product_detail" and self.parent_obj:
  #     kwargs["queryset"] = self.parent_obj.product_cagetory.allproductsdetails() 
  #   return super(PostProduct, self).formfield_for_manytomany(db_field, request, **kwargs)

  form = ProductAdminForm
  # exclude = ('product_detail',)
  inlines = [ProductImageInLine,ProductPromotionInLine]


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

    # def get_formset(self, request, obj=None, **kwargs):
    #   self.parent_obj = obj
    #   print (super(admin.TabularInline, self))
    #   return super(admin.TabularInline, self).get_formset(request, obj, **kwargs)


    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #   if db_field.name == "product_detail" and self.parent_obj:
    #     kwargs["queryset"] = self.parent_obj.allproductsdetails() 
    #   return super(admin.TabularInline, self).formfield_for_manytomany(db_field, request, **kwargs)

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
admin.site.register(ProductSpecific,MyModelAdmin)
admin.site.register(ProductSpecificDetail,MyModelAdmin)
admin.site.register(ProductPromotion)
admin.site.register(Agency,AgencyAdmin)