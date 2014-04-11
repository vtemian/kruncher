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
  from map.jobs.sum import GroupSum
  job = GroupSum(0, [1, 2])
  job.run(input=['data:8a969fe6-3b5d-4793-937b-6400ef85403d'])

  from disco.core import result_iterator

  lines = []
  for word, line in result_iterator(job.wait(show=True)):
    lines.append(line)

  return json.dumps({
      'status': 'success',
      'message': json.dumps(lines)
  })
