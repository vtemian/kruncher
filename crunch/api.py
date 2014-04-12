import json

import rethinkdb as r
from flask import Blueprint

from utils.decorators import validate, require
from utils.validators import simple_validation, validate_uuid
from utils.tasks import execute_async

from krunchr.vendors.rethinkdb import db
import crunch.jobs.add

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
  dataset = r.table('datasets').get(ds_id).run(db.conn)

  fields = [str(dataset['fields'].index(field)) for field in fields]
  group_by = dataset['fields'].index(group_by)

  command = "python sum.py %s %s %s" % (ds_id, group_by,
				        ' '.join(fields))
  #execute_async.delay(command)
  crunch.jobs.add.try_me([ds_id, group_by] + fields)

  return json.dumps({
      'status': 'success',
      'message': command,
  })
