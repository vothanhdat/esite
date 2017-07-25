from django.contrib import admin
from ..models import Brand
from tagging.fields import TagField
from util.wiget.autocomplete import AutoTaggingWiget

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
  formfield_overrides = {
    TagField: {'widget': AutoTaggingWiget('econ:tag-ac')},
  }