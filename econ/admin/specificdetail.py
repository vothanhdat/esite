from django.contrib import admin
from django import forms
from django.contrib.admin.sites import site
from util.wiget.autocomplete import AutoCompleteWiget,Exclude
from econ.models import Specific, SpecificDetail, ProductSpecDetail

class SpecificDetailForm(forms.ModelForm):
  class Meta:
    fields = ('specof','spec','desc')

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
      

class SpecificDetailInline(admin.TabularInline):
  model = ProductSpecDetail
  form = SpecificDetailForm
  extra = 1





