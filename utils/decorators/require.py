from functools import wraps

from flask import request

from utils.exceptions import HttpBadRequest


class require(object):

  def __init__(self, *requires):
    self.requires = requires

  def get_arguments(self):
    if request.method in ['POST', 'PUT']:
      return request.data
    return request.args

  def __call__(self, f):
    @wraps(f)
    def decorated(*args, **kwargs):
      errors = []
      arguments = self.get_arguments()

      for param in self.requires:
        if param not in arguments:
          errors.append('%s is required' % param)

      if errors:
        raise HttpBadRequest("\n".join(errors))

      result = f(*args, **kwargs)
      return result
    return decorated
