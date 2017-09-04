from django import forms
from django.contrib import admin
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.admin import GenericTabularInline
from util.wiget.slugwidget import SlugWiget
from util.abstractmodels import Slug


class SlugInline(GenericTabularInline):
    model = Slug


class SlugFieldFormMixin(forms.Form):
  slug_field = forms.CharField(widget=SlugWiget)

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
    slug = form.instance.slug.first()
    if slug : 
      slug.slug = self.cleaned_data.get('slug_field', None)
      slug.save()
    else :
      Slug.objects.create(
        content_object=form.instance, 
        slug=self.cleaned_data.get('slug_field', None)
      )


class SlugFieldListFormMixin(forms.Form):

  slug_field = forms.CharField(widget=SlugWiget)

  def __init__(self, *args, **kwargs):
    instance = kwargs.get('instance')
    if instance:
      if instance.id:
        initial = kwargs.get('initial', {})
        initial['slug_field'] = instance.slug.first() 
      kwargs['initial'] = initial
    super(SlugFieldFormMixin, self).__init__(*args, **kwargs)


  def save_related(self, *args, **kwargs):
    slug = self.instance.slug.first()
    if slug : 
      slug.slug = self.cleaned_data.get('slug_field', None)
      slug.save()
    else :
      Slug.objects.create(
        content_object=form.instance, 
        slug=self.cleaned_data.get('slug_field', None)
      )
      super(SlugFieldListFormMixin, self).save(*args, **kwargs)
