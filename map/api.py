import json

import rethinkdb as r
from flask import Blueprint

from utils.decorators import validate, require
from utils.validators import simple_validation, validate_uuid
from utils.tasks import execute_async

from krunchr.vendors.rethinkdb import db

endpoint = Blueprint('maps_jobs', __name__)


@endpoint.route('map/group_by/', methods=['POST'])
@require('fields', 'operation', 'ds_id', 'group_by')
@validate({
    'fields': simple_validation,
    'operation': simple_validation,
    'ds_id': validate_uuid,
    'group_by': simple_validation,
})
def map(fields, operation, ds_id, group_by):
  dataset = r.table('datasets').filter({
      'ds_id': ds_id
  }).run(db.conn)

  fields = [dataset['fields'].index(field) for field in fields]
  group_by = dataset['fields'].index(group_by)

  command = "python map/jobs/sum.py %s %s %s" % (ds_id, group_by,
                                                 ' '.join(fields))
  execute_async.delay(command)

  return json.dumps({
      'status': 'success',
  })
