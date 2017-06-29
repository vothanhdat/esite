from django.contrib import admin
from .models import Brand,Cagetory,Product,ProductImage,BaseUser,Agency,AgencyMember


class PostProduct(admin.ModelAdmin):
    class ProductImageInLine(admin.StackedInline):
      model = ProductImage
      fields = ['image']
    inlines = [ProductImageInLine]

class BaseUserMemberof(admin.ModelAdmin):
    class BaseUserMemberInline(admin.StackedInline):
      model = AgencyMember
      fk_name = 'user'
      exclude = ('inviter',)
    inlines = [BaseUserMemberInline]


class AgencyMembers(admin.ModelAdmin):
    class AgencyMembersInline(admin.StackedInline):
      model = AgencyMember
      fk_name = 'agency'
      exclude = ('inviter',)
    inlines = [AgencyMembersInline]

admin.site.register(Brand)
admin.site.register(Cagetory)
admin.site.register(BaseUser,BaseUserMemberof)
admin.site.register(Product,PostProduct)
admin.site.register(Agency,AgencyMembers)