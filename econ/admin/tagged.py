from django.db import models
from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.forms import Textarea
from django.contrib.contenttypes.admin  import GenericStackedInline, BaseGenericInlineFormSet
from ..models import TaggedInfo

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
    model = TaggedInfo
    max_num = 1
    verbose_name = "SEO Info"
    verbose_name_plural = "TAGGED"
    formset = RequiredInlineFormSet




    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }



class TagInlineParent(TagInline):
    fields = ('parent_tags','tags','slug',)
    readonly_fields = ('parent_tags',)

    def parent_tags(self):
        raise 'sssssssssssssssss'

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super(TagInlineParent, self).get_formset(request, obj, **kwargs)