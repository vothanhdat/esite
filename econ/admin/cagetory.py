
from django import forms
from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
# from import_export.admin import ImportExportActionModelAdmin
from django.contrib.admin import SimpleListFilter
from ..models import Cagetory

from tagging.fields import TagField
from util.wiget.autocomplete import AutoTaggingWiget
from util.admin.slug  import SlugFieldFormMixin
from util.admin.admin_customtreefilter import CustomTreeRelatedFieldListFilter



class CagetoryForm(forms.ModelForm,SlugFieldFormMixin):
  pass

class CagetoryIsLeafFilter(SimpleListFilter):
  title = 'Leaf node'
  parameter_name = 'leaf'
  def lookups(self, request, model_admin):
    return (
        ("1", "Leaf"),
        ("0", "Not Leaf"),
    )

  def queryset(self, request, queryset):
    if self.value() == "1":
      return queryset.extra(where=['econ_cagetory.rght - econ_cagetory.lft = 1'])
    elif self.value() == "0":
      return queryset.extra(where=['econ_cagetory.rght - econ_cagetory.lft <> 1'])
    else:
      return queryset


@admin.register(Cagetory)
class CagetoryAdmin(DjangoMpttAdmin):
  form = CagetoryForm
  tree_auto_open = False
  formfield_overrides = {
    TagField: {'widget': AutoTaggingWiget('econ:tag-ac')},
  }
  list_display = ('name','allow_choose',  'slug_field','tags','optiontype','parent','is_leaf_node' )
  list_editable = ('allow_choose' ,)
  list_filter = (
    CagetoryIsLeafFilter,
    'allow_choose',
    'optiontype'
  )

  def get_queryset(self, request):
    qs = super(CagetoryAdmin, self).get_queryset(request)
    return qs.prefetch_related(
      'slug'
    ) .select_related(
      'parent'
    )
