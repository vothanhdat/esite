from django.contrib import admin
from util.admin.admin_customtreefilter import InheritTreeRelatedFieldListFilter
from ..models import Customer,AgencyMember
# class CustomerMemberInline(admin.StackedInline):
#   model = AgencyMember
#   fk_name = 'user'
#   exclude = ('inviter',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
  # inlines = [CustomerMemberInline]
  extra = 1