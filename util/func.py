import uuid
import base64
try:
    import urlparse
    from urllib import urlencode
except: # For Python 3
    import urllib.parse as urlparse
    from urllib.parse import urlencode

import string
import random

def rabdombase64():
  lst = [random.choice(string.ascii_letters + string.digits) for n in range(30)]
  str = "".join(lst)
  return str

def addparamtourl(url,params):
  url_parts = list(urlparse.urlparse(url))
  query = dict(urlparse.parse_qsl(url_parts[4]))
  query.update(params)
  url_parts[4] = urlencode(query)
  return urlparse.urlunparse(url_parts)


import functools
import weakref

def memoized_method(*lru_args, **lru_kwargs):
  def decorator(func):
    @functools.wraps(func)
    def wrapped_func(self, *args, **kwargs):
      # We're storing the wrapped method inside the instance. If we had
      # a strong reference to self the instance would never die.
      self_weak = weakref.ref(self)
      @functools.wraps(func)
      @functools.lru_cache(*lru_args, **lru_kwargs)
      def cached_method(*args, **kwargs):
        return func(self_weak(), *args, **kwargs)
      setattr(self, func.__name__, cached_method)
      return cached_method(*args, **kwargs)
    return wrapped_func
  return decorator
