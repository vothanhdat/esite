from django import forms
from django.contrib import admin
from ..models import Brand
from util.abstractmodels import Slug
from tagging.fields import TagField
from util.wiget.autocomplete import AutoTaggingWiget
from util.admin.slug  import SlugFieldFormMixin

class BrandForm(SlugFieldFormMixin, forms.ModelForm):
  pass

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
  form = BrandForm
  formfield_overrides = {
    TagField: {'widget': AutoTaggingWiget('econ:tag-ac')},
  }
  list_display = ('name','slug_field','tags' )
