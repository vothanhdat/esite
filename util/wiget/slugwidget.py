from django.forms.widgets import TextInput


class SlugWiget(TextInput):

    def __init__(self, attrs=None):

        super(SlugWiget, self).__init__(attrs)


    class Media:
        js = (
            'admin/custom-slug.js',
        )


    def build_attrs(self, *args, **kwargs):
        attrs = super(SlugWiget, self).build_attrs(*args, **kwargs)
        custom_attrs = {
            'data-slug':True,
            'data-slugdes':'name',
        }
        attrs.update(custom_attrs)
        return attrs