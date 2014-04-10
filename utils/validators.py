import urlparse


class ValidationError(Exception):
  pass


def validate_url(url):
  _url = urlparse.urlsplit(url, 'http')
  if _url.scheme != 'http':
    raise ValidationError("Invalid scheme '%s', should be http" % _url.scheme)
  elif not url.startswith('http://'):
    _url = urlparse.urlsplit('http://%s' % url, 'http')

  return _url
