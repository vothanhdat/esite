from django import forms
from django.contrib import admin
from ..models import AgencyMember, AgencyPromotion,Agency

from .slug  import SlugFieldFormMixin

class AgencyForm(SlugFieldFormMixin, forms.ModelForm):
  pass


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
    
  form = AgencyForm
  inlines = [AgencyMembersInline,AgencyPromotionsInline]
