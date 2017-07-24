
import json
from django.contrib.admin import widgets
from tagging.models import Tag
from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from zinnia.models import Entry
from django.forms import Media


class TagAutoComplete(widgets.AdminTextInputWidget):
    """
    Tag widget with autocompletion based on select2.
    """

    def get_tags(self):
        """
        Returns the list of tags to auto-complete.
        """
        return [tag.name for tag in
                Tag.objects.usage_for_model(Entry)]

    def render(self, name, value, attrs=None):
        """
        Render the default widget and initialize select2.
        """
        if not attrs:
            attrs = {}

        attrs['multiple']= True
        attrs['data-tagginginfo']= True
        attrs['data-data']= json.dumps(self.get_tags())

        return super(TagAutoComplete,self).render(name, value,attrs)
        # output = [super(TagAutoComplete, self).render(name, value, attrs)]
        # output = ['<select  multiple id="id_%s" data-data=\'[{"id": "1", "text": "One"}, {"id": "2", "text": "Two"}]\' data-tags="true"></select>' % name]
        # output.append('<script type="text/javascript">')
        # output.append('(function($) {')
        # output.append('  $(document).ready(function() {')
        # output.append('    $("#id_%s").select2({' % name)
        # # output.append('       width: "element",')
        # # output.append('       tokenSeparators: [",", " "],')
        # output.append('       tags: %s,' % json.dumps(self.get_tags()))
        # # output.append('       tags: true,')
        # output.append('       });')
        # output.append('    });')
        # output.append('}(django.jQuery));')
        # output.append('</script>')


        # output.append('<script type="text/javascript">')
        # output.append('(function($) {')
        # output.append('  $(document).ready(function() {')
        # output.append('    $("#id_%s").select2({' % name)
        # output.append('       width: "element",')
        # output.append('       maxi
        # output.append('       tokenSeparators: [",", " "],')
        # output.append('       tags: %s' % json.dumps(self.get_tags()))
        # output.append('    mumInputLength: 50,') });')
        # output.append('    });')
        # output.append('}(django.jQuery));')
        # output.append('</script>')
        # return mark_safe('\n'.join(output))
        # return mark_safe('<select data-data=\'[{"id": "1", "text": "One"}, {"id": "2", "text": "Two"}]\' data-tags="true"></select>')


    @property
    def media(self):
        """
        TagAutoComplete's Media.
        """

        return Media(
            # css={'all': (static('css/select2.css'),)},
            js=('admin/custom-tagging.js',)
        )

