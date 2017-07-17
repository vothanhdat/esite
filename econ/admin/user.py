from django.contrib import admin
from util.admin.admin_customtreefilter import InheritTreeRelatedFieldListFilter
from ..models import BaseUser,AgencyMember

@admin.register(BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
  class BaseUserMemberInline(admin.StackedInline):
    model = AgencyMember
    fk_name = 'user'
    exclude = ('inviter',)
  inlines = [BaseUserMemberInline]
  extra = 1