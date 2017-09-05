from dal import autocomplete, forward


class Exclude(forward.Forward):
    type = "exclude"
    def __init__(self, exclude,parent=None,isExactly = False):
        self.exclude = exclude
        self.parent = parent
        self.ext = isExactly
        
    def to_dict(self):
        d = super(Exclude, self).to_dict()
        d.update(exclude=self.exclude)
        if self.parent:
            d.update(parent=self.parent)
        if self.ext:
            d.update(ext=self.ext)
        return d

class Include(forward.Forward):
    type = "include"
    def __init__(self, include,parent=None,isExactly = False):
        self.include = include
        self.parent = parent
        self.ext = isExactly
    def to_dict(self):
        d = super(Include, self).to_dict()
        d.update(include=self.include)
        if self.parent:
            d.update(parent=self.parent)
        if self.ext:
            d.update(ext=self.ext)
        return d


forward.Exclude = Exclude
forward.Include = Include


class AutoCompleteWiget(autocomplete.ModelSelect2):
  autocomplete_function = 'customselect2'
  class Media:
    js = (
        'admin/custom-select.js',
    )

class AutoCompleteMutipleWiget(autocomplete.ModelSelect2Multiple):
  autocomplete_function = 'customselect2'
  class Media:
    js = (
        'admin/custom-select.js',
    )



class AutoTaggingWiget(autocomplete.TaggingSelect2):
  autocomplete_function = 'customtagging2'

  def custom_attrs(self, *args, **kwargs):
    return {}

  def build_attrs(self, *args, **kwargs):
    attrs = super(AutoTaggingWiget, self).build_attrs(*args, **kwargs)
    custom_attrs = self.custom_attrs(*args, **kwargs)
    attrs.update(custom_attrs)
    return attrs

  class Media:
    js = (
        'admin/custom-select.js',
    )
    css = {
      'all':('admin/custom-select.css',)
    }
    pass
