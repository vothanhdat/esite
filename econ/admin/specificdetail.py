from django.contrib import admin
from django import forms
from django.contrib.admin.sites import site
from util.wiget.autocomplete import AutoCompleteWiget,Exclude,Include
from econ.models import Specific, SpecificDetail, ProductSpecDetail
from nested_admin.nested import NestedModelAdmin,NestedInlineModelAdmin,NestedStackedInline,NestedTabularInline

class SpecificDetailForm(forms.ModelForm):
  class Meta:
    fields = ('specof','spec','desc')
    # fields = ('spec','desc')

  specofwidget = AutoCompleteWiget(
    'econ:spec-ac',
    forward=[
      'product_cagetory',
      'prod',
      Exclude(exclude='productspecdetail_set---specof')
    ],
  )

  specwiget = AutoCompleteWiget(
    'econ:prodspecdeit-ac',
    forward=['specof']
  )

  specof = forms.ModelChoiceField(queryset=Specific.objects.all(),widget = specofwidget)
  spec = forms.ModelChoiceField(queryset=SpecificDetail.objects.all(),widget = specwiget)

  def get_initial_for_field(self,field, field_name):
    instance = self.instance
    if instance and field_name == 'specof' and instance.spec_id:
      return instance.spec.detail_field
    else:
      return super(SpecificDetailForm,self).get_initial_for_field(field, field_name)
      

class SpecificDetailInline(NestedTabularInline):
  model = ProductSpecDetail
  form = SpecificDetailForm
  extra = 1

class OptionSpecificDetailInline(NestedTabularInline):
  class OptionSpecificDetailForm(SpecificDetailForm):

    specofwidget = AutoCompleteWiget(
      'econ:spec-ac',
      forward=[
        'product_cagetory',
        'prod',
        Include(include='productspecdetail_set---specof'),
        Exclude(exclude='productoption_set---specof'),
      ],
    )

    specof = forms.ModelChoiceField(queryset=Specific.objects.all(),widget = specofwidget)

  model = ProductSpecDetail
  form = OptionSpecificDetailForm
  extra = 1





