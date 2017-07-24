from django.db import models
from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.forms import Textarea
from django.contrib.contenttypes.admin  import GenericStackedInline, BaseGenericInlineFormSet
# from zinnia.admin.widgets import TagAutoComplete
from ..widget.TaggingWiget import TagAutoComplete
from django import forms

from ..models import TaggedInfo



class TaggedInfoForm(forms.ModelForm):
    class Meta:
        """
        EntryAdminForm's Meta.
        """
        fields = forms.ALL_FIELDS
        model = TaggedInfo
        widgets = {
            'tags': TagAutoComplete,
        }


class RequiredInlineFormSet(BaseGenericInlineFormSet):
    """
    Generates an inline formset that is required
    """

    def _construct_form(self, i, **kwargs):
        """
        Override the method to change the form attribute empty_permitted
        """
        form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form



class TagInline(GenericStackedInline):
    form = TaggedInfoForm
    model = TaggedInfo
    # formset = RequiredInlineFormSet
    max_num = 1
    verbose_name = "SEO Info"
    verbose_name_plural = "TAGGED"



class TagInlineParent(TagInline):
    
    # fields = ('slug',)
    # readonly_fields = ('parent_tags',)

    # def parent_tags(self):
    #     raise 'sssssssssssssssss'

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super(TagInlineParent, self).get_formset(request, obj, **kwargs)