
from django import forms
from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from ..models import Cagetory

from tagging.fields import TagField
from util.wiget.autocomplete import AutoTaggingWiget
from .slug  import SlugFieldFormMixin



class CagetoryForm(SlugFieldFormMixin, forms.ModelForm):
  pass


@admin.register(Cagetory)
class CagetoryAdmin(DjangoMpttAdmin):
  form = CagetoryForm
  tree_auto_open = False
  formfield_overrides = {
    TagField: {'widget': AutoTaggingWiget('econ:tag-ac')},
  }
  list_display = ('cagetory_name', 'tags', 'slug_field','optiontype','parent' )
  # list_editable = ('slug','tags', 'optiontype','parent' )
  def slug_field(self, instance):
    return instance.slug.first()
