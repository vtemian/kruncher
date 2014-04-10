import json
from functools import wraps

from flask import request

from utils.exceptions import HttpBadRequest
from utils.validators import ValidationError


class validation(object):

  def __init__(self, rules):
    self.rules = rules

  def get_params(self):
    if request.method in ['POST', 'PUT']:
      return json.loads(request.data)
    return request.args

  def __call__(self, f):

    @wraps(f)
    def decorated(*args, **kwargs):
      errors = []
      params = self.get_params()

      for param in self.rules:
        try:
          kwargs[param] = self.rules[param](params.get(param, ''))
        except ValidationError as e:
          errors.append(e.message)

      if errors:
        raise HttpBadRequest("\n".join(errors))

      return f(*args, **kwargs)

    return decorated
