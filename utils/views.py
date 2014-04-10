import json

from flask import request, Response


def get_request_type():
  types = {
      'application/json': 'json',
      'application/xml': 'xml'
  }

  if 'Content-Type' in request.headers:
    if request.headers['Content-Type'] in types:
      return types[request.headers['Content-Type']]

  return 'html'


def serialize_response(request_type, response):
  serializers = {
      'json': lambda response: json.dumps(response),
      'xml': lambda response: json.dumps(response),
  }

  if isinstance(response, basestring) or isinstance(response, Response):
    return response

  if request_type in serializers:
    return serializers[request_type](response)

  return json.dumps(response)
