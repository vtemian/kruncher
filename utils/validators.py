import urlparse


class ValidationError(Exception):
  pass


def validate_url(url):
  _url = urlparse.urlsplit(url, 'http')
  if _url.scheme not in ['http', 'https']:
    raise ValidationError("Invalid scheme '%s', should be http or https" %
                          _url.scheme)

  return url


def validate_uuid(uuid):
  return uuid


def simple_validation(val):
  return val
