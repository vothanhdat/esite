from django.contrib import admin
from django.utils.html import format_html_join,format_html

from util.admin.admin_customtreefilter import InheritTreeRelatedFieldListFilter
from ..models import Specific,SpecificDetail

@admin.register(Specific)
class SpecificAdmin(admin.ModelAdmin):
  list_display = ['specific_name', 'specific_of'] 
  list_filter = [ ('specific_of', InheritTreeRelatedFieldListFilter)]
  readonly_fields=('all_specific',)
 
  def all_specific(self, instance):

    if instance.specificdetail_set:
        queryset = instance.specificdetail_set.all()
        return format_html_join('','<p>{}</p>',((u,) for u in queryset))
    else:
        return '---------------'

  
