from django.contrib import admin
from util.admin.admin_customtreefilter import InheritTreeRelatedFieldListFilter
from ..models import Specific

@admin.register(Specific)
class SpecificAdmin(admin.ModelAdmin):
  list_display = ['specific_name', 'specific_of'] 
  list_filter = [ ('specific_of', InheritTreeRelatedFieldListFilter)]
  
