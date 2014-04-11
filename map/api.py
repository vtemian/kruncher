import json

from flask import Blueprint

from utils.decorators import validate, require
from utils.validators import simple_validation, validate_uuid

endpoint = Blueprint('maps_jobs', __name__)


@endpoint.route('map/', methods=['POST'])
@require('fields', 'operation', 'ds_id')
@validate({
    'fields': simple_validation,
    'operation': simple_validation,
    'ds_id': validate_uuid,
})
def map(fields, operation, ds_id):
  return json.dumps({
      'status': 'success'
  })
