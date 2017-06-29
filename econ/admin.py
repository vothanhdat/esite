from django.contrib import admin
from .models import Brand,Cagetory,Product,ProductImage,BaseUser,Agency,AgencyMember,AgencyPromotion,ProductPromotion


class PostProduct(admin.ModelAdmin):
    class ProductImageInLine(admin.StackedInline):
      model = ProductImage
      fields = ['image']
    class ProductPromotionInLine(admin.StackedInline):
      model = ProductPromotion.apply_to.through
      # fields = ['apply_to']
      
      # filter_horizontal = ('apply_to',)
      # fields = ['apply_to']

    inlines = [ProductImageInLine,ProductPromotionInLine]

class BaseUserAdmin(admin.ModelAdmin):
    class BaseUserMemberInline(admin.StackedInline):
      model = AgencyMember
      fk_name = 'user'
      exclude = ('inviter',)
    inlines = [BaseUserMemberInline]


class AgencyAdmin(admin.ModelAdmin):
    class AgencyMembersInline(admin.StackedInline):
      model = AgencyMember
      fk_name = 'agency'
      exclude = ('inviter',)
    class AgencyPromotionsInline(admin.StackedInline):
      model = AgencyPromotion
      fk_name = 'apply_to'
      
    inlines = [AgencyMembersInline,AgencyPromotionsInline]


admin.site.register(Brand)
admin.site.register(Cagetory)
admin.site.register(BaseUser,BaseUserAdmin)
admin.site.register(Product,PostProduct)
admin.site.register(ProductPromotion)
admin.site.register(Agency,AgencyAdmin)