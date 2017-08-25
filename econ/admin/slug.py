from django import forms
from django.contrib import admin
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.admin import GenericTabularInline

from ..models import Slug

class SlugInline(GenericTabularInline):
    model = Slug


class SlugFieldFormMixin(forms.Form):
  slug_field = forms.CharField()

  def get_initial_for_field(self,field, field_name):
    instance = self.instance
    if field_name == 'slug_field' and instance and instance.id:
      return instance.slug.first() 
    else:
      return super(SlugFieldFormMixin,self).get_initial_for_field(field, field_name)
      

  def clean_slug_field(self):
    slug = slugify(self.cleaned_data['slug_field'])
    if self.instance :
      first = Slug.objects.filter(slug=slug).first()

      if first and first.content_object != self.instance:
        raise forms.ValidationError("Slug already exists")
    elif Slug.objects.filter(slug=slug).exists():
      raise forms.ValidationError("Slug already exists")
    return slug

  def save_related(self, request, form, formsets, change):
    Slug.objects.create(
      content_object=form.instance, 
      slug=self.cleaned_data.get('slug_field', None)
    )
