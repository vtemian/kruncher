import json

from flask import Blueprint, current_app

from utils.decorators import validate, require
from utils.validators import validate_url, validate_uuid

from .tasks import get_file, push_data, get_fields

endpoint = Blueprint('analyse_url', __name__)


@endpoint.route('analyse/', methods=['POST'])
@require('url', 'ds_id')
@validate({
    'url': validate_url,
    'ds_id': validate_uuid
})
def analyse_url(url, ds_id):
  (get_fields.s(url, ds_id) |
   get_file.s(current_app.config['DISCO_FILES']) |
   push_data.s()).apply_async()

  return json.dumps({
      'status': 'success'
  })
