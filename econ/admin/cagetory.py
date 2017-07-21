
from django_mptt_admin.admin import DjangoMpttAdmin
from django.contrib import admin
from ..models import Cagetory
from .tagged import TagInlineParent



@admin.register(Cagetory)
class CagetoryAdmin(DjangoMpttAdmin):
  class CagetoryTagInline(TagInlineParent):
    def parent_tags(self,instance):
      if self.parent_obj : 
        return instance.parent_tags(self.parent_obj)
      
  tree_auto_open = False
  inlines=[CagetoryTagInline]