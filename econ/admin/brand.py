from django import forms
from django.contrib import admin
from ..models import Brand,Slug
from tagging.fields import TagField
from util.wiget.autocomplete import AutoTaggingWiget
from .slug  import SlugFieldFormMixin

class BrandForm(SlugFieldFormMixin, forms.ModelForm):
  pass

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
  form = BrandForm
  formfield_overrides = {
    TagField: {'widget': AutoTaggingWiget('econ:tag-ac')},
  }
  list_display = ('name','slug_field','tags' )

  def slug_field(self,instance):
    return instance.slug.first()
  # list_editable = ('slug', 'tags' )

  # # inlines=[SlugModel,]
  # def slug(self, x):
  #   return x.slug

# admin.site.register(SlugModel)
