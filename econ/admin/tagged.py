from django.db import models
from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.forms import Textarea
from django.contrib.contenttypes.admin  import GenericStackedInline, BaseGenericInlineFormSet
from django import forms
from dal import autocomplete
from ..models import TaggedInfo
from util.wiget.autocomplete import AutoTaggingWiget
from tagging.models import Tag
from django.core.cache import cache




# def allTagging():
#     value = cache.get('alltagging')
#     if value:
#         return value
#     else:
#         value = ','.join([e['name'] for e in Tag.objects.all().values('name')])
#         cache.set('alltagging',value,60)
#         return value
        

# class TagInlineWiget(AutoTaggingWiget):
#     def custom_attrs(self, *args, **kwargs):
#         return { 'data-availabletags' : allTagging() }

class TaggedInfoForm(autocomplete.FutureModelForm):

    class Meta:
        """
        EntryAdminForm's Meta.
        """
        fields = forms.ALL_FIELDS
        model = TaggedInfo
        widgets = {
            'tags': AutoTaggingWiget('econ:tag-ac')
        }


class RequiredInlineFormSet(BaseGenericInlineFormSet):
    """
    Generates an inline formset that is required
    """

    def _construct_form(self, i, **kwargs):
        """
        Override the method to change the form attribute empty_permitted
        """
        form = super(RequiredInlineFormSet,self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form

class TagInline(GenericStackedInline):
    model = TaggedInfo
    




    form = TaggedInfoForm
    formset = RequiredInlineFormSet
    max_num = 1
    verbose_name = "SEO Info"
    verbose_name_plural = "TAGGED"



class TagInlineParent(TagInline):
    
    fields = ('slug','parent_tags','tags',)
    readonly_fields = ('parent_tags',)

    def parent_tags(self):
        raise 'sssssssssssssssss'

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super(TagInlineParent, self).get_formset(request, obj, **kwargs)