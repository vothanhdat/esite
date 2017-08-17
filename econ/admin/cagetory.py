
from django_mptt_admin.admin import DjangoMpttAdmin
from django.contrib import admin
from ..models import Cagetory

from tagging.fields import TagField
from util.wiget.autocomplete import AutoTaggingWiget

@admin.register(Cagetory)
class CagetoryAdmin(DjangoMpttAdmin):

  tree_auto_open = False
  formfield_overrides = {
    TagField: {'widget': AutoTaggingWiget('econ:tag-ac')},
  }
  list_display = ('cagetory_name', 'tags', 'slug','optiontype','parent' )
  list_editable = ('slug','tags', 'optiontype','parent' )
