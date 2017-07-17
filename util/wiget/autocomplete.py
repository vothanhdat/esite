from dal import autocomplete, forward


class Exclude(forward.Forward):
    type = "exclude"
    def __init__(self, exclude):
        self.exclude = exclude
    def to_dict(self):
        d = super(Exclude, self).to_dict()
        d.update(exclude=self.exclude)
        return d


forward.Exclude = Exclude


class AutoCompleteWiget(autocomplete.ModelSelect2):
  autocomplete_function = 'customselect2'
  class Media:
    js = (
        'custom.js',
    )
    css = {
      'all': (
        'custom.css',
      )
    }