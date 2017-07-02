from django.contrib import admin
from django import forms

from .models import Brand,Cagetory,Product,ProductImage,BaseUser,Agency,AgencyMember,AgencyPromotion,ProductPromotion,ProductSpecific,ProductSpecificDetail

class MyModelAdmin(admin.ModelAdmin):
  def get_model_perms(self, request):
    return {}


class PostProduct(admin.ModelAdmin):
  class ProductImageInLine(admin.StackedInline):
    model = ProductImage
    fields = ['image']
    extra = 1
  class ProductPromotionInLine(admin.StackedInline):
    model = ProductPromotion.apply_to.through
    extra = 1

  def get_form(self, request, obj=None, **kwargs):
    self.parent_obj = obj
    print super(PostProduct, self)
    return super(PostProduct, self).get_form(request, obj, **kwargs)


  def formfield_for_manytomany(self, db_field, request, **kwargs):
    if db_field.name == "product_detail" and self.parent_obj:
      kwargs["queryset"] = ProductSpecificDetail.objects.filter(detail_field__specific_of=self.parent_obj.product_cagetory)
    return super(PostProduct, self).formfield_for_manytomany(db_field, request, **kwargs)

  
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


admin.site.register(Brand)
admin.site.register(Cagetory)
admin.site.register(BaseUser,BaseUserAdmin)
admin.site.register(Product,PostProduct)
admin.site.register(ProductSpecific,MyModelAdmin)
admin.site.register(ProductSpecificDetail,MyModelAdmin)
admin.site.register(ProductPromotion)
admin.site.register(Agency,AgencyAdmin)