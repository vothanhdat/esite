import uuid
import base64
try:
    import urlparse
    from urllib import urlencode
except: # For Python 3
    import urllib.parse as urlparse
    from urllib.parse import urlencode


def rabdombase64():
  return base64.b64encode(uuid.uuid4().bytes).replace('=', '')

def addparamtourl(url,params):
  url_parts = list(urlparse.urlparse(url))
  query = dict(urlparse.parse_qsl(url_parts[4]))
  query.update(params)
  url_parts[4] = urlencode(query)
  return urlparse.urlunparse(url_parts)
