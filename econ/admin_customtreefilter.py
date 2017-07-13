from mptt.admin import TreeRelatedFieldListFilter,TreeNodeChoiceField
from django.utils.translation import ugettext as _, ugettext_lazy
from django.utils.encoding import smart_text
from django.db.models.fields.related import ForeignObjectRel, ManyToManyField
from mptt.compat import remote_field, remote_model
from django.utils.translation import get_language_bidi
from django.utils.html import format_html, mark_safe


    


class CustomTreeRelatedFieldListFilter(TreeRelatedFieldListFilter):
  template='custom_mptt_filter.html'
  
  def field_choices(self, field, request, model_admin):

    return field.related_model._default_manager.filter(level__lte=0)

  def choice_recuser(self,lookup_choices, cl,EMPTY_CHANGELIST_VALUE):
    for model in lookup_choices:

      yield {
        'query_string': cl.get_query_string({
          self.changed_lookup_kwarg: model.id,
        }, [self.lookup_kwarg_isnull]),
        'display': model,
        'selected': (long(self.lookup_val) == model.id) if self.lookup_val else False,
        'child': self.choice_recuser(
          model.get_children().all(),
          cl,
          EMPTY_CHANGELIST_VALUE
        ) if model.get_descendant_count() else None,
      }


  def choices(self, cl):
    EMPTY_CHANGELIST_VALUE = self.empty_value_display
    yield {
      'selected': self.lookup_val is None and not self.lookup_val_isnull,
      'query_string': cl.get_query_string({
        self.changed_lookup_kwarg: None,
      }, [self.lookup_kwarg, self.lookup_kwarg_isnull]),
      'display': _('All'),
    }
    for choice in self.choice_recuser(self.lookup_choices,cl,EMPTY_CHANGELIST_VALUE):
      yield choice
