from django.contrib import admin
from django import forms
from django.contrib.admin.sites import site
from util.wiget.autocomplete import AutoCompleteWiget,Exclude,Include
from econ.models import Specific, SpecificDetail, ProductOptionSpecDetail
from nested_admin.nested import NestedModelAdmin,NestedInlineModelAdmin,NestedStackedInline,NestedTabularInline


class OptionSpecificDetailForm(forms.ModelForm):

  specofwidget = AutoCompleteWiget(
    'econ:spec-ac',
    forward=[
      'spec_types',
      Exclude(exclude='productoption_set---specof')
    ],
  )

  specwiget = AutoCompleteWiget(
    'econ:prodspecdeit-ac',
    forward=['specof']
  )

  specof = forms.ModelChoiceField(queryset=Specific.objects.all(),widget = specofwidget)
  spec = forms.ModelChoiceField(queryset=SpecificDetail.objects.all(),widget = specwiget)

  class Meta:
    fields = ('specof','spec','desc')

  def get_initial_for_field(self,field, field_name):
    instance = self.instance
    if instance and field_name == 'specof' and instance.spec_id:
      return instance.spec.detail_field
    else:
      return super(OptionSpecificDetailForm,self).get_initial_for_field(field, field_name)


      
class OptionSpecificDetailInline(NestedTabularInline):

  model = ProductOptionSpecDetail
  form = OptionSpecificDetailForm
  extra = 1



