from django.contrib import admin
from ..models import AgencyMember, AgencyPromotion,Agency



@admin.register(Agency)
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
