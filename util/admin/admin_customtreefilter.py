from mptt.admin import TreeRelatedFieldListFilter,TreeNodeChoiceField
from django.utils.translation import ugettext as _, ugettext_lazy
from django.utils.encoding import smart_text
from django.db.models.fields.related import ForeignObjectRel, ManyToManyField
from mptt.compat import remote_field, remote_model
from django.utils.translation import get_language_bidi
from django.utils.html import format_html, mark_safe
from django.contrib.admin.utils import get_model_from_relation
from django.contrib.admin.options import IncorrectLookupParameters
from django.core.exceptions import ValidationError


    


class CustomTreeRelatedFieldListFilter(TreeRelatedFieldListFilter):
  template='custom/custom_mptt_filter.html'
  
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



class InheritTreeRelatedFieldListFilter(CustomTreeRelatedFieldListFilter):
  def __init__(self, field, request, params, model, model_admin, field_path):

    self.other_model = get_model_from_relation(field)
    if remote_field(field) is not None and hasattr(remote_field(field), 'get_related_field'):
        self.rel_name = remote_field(field).get_related_field().name
    else:
        self.rel_name = self.other_model._meta.pk.name
    self.changed_lookup_kwarg = '%s__%s__inherit' % (field_path, self.rel_name)
    super(InheritTreeRelatedFieldListFilter, self).__init__(field, request, params,
                                                      model, model_admin, field_path)
    self.lookup_val = request.GET.get(self.changed_lookup_kwarg)


  def queryset(self, request, queryset):
    try:
      # #### MPTT ADDITION START
      if self.lookup_val:
        other_model = self.other_model.objects.get(pk=self.lookup_val)
        other_models = other_model.get_ancestors(True, include_self=True).values('id')
        print other_models
        del self.used_parameters[self.changed_lookup_kwarg]
        self.used_parameters.update(
          {'%s__%s__in' % (self.field_path, self.rel_name): other_models}
        )
      # #### MPTT ADDITION END
      return queryset.filter(**self.used_parameters)
    except ValidationError as e:
      raise IncorrectLookupParameters(e)
