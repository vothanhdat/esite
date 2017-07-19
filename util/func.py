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
  lst = [random.choice(string.ascii_letters + string.digits) for n in xrange(30)]
  str = "".join(lst)
  return str

def addparamtourl(url,params):
  url_parts = list(urlparse.urlparse(url))
  query = dict(urlparse.parse_qsl(url_parts[4]))
  query.update(params)
  url_parts[4] = urlencode(query)
  return urlparse.urlunparse(url_parts)
