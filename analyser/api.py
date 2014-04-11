import os
import json

import requests
import rethinkdb as r

from flask import Blueprint, current_app

from utils.decorators import validate, require
from utils.validators import validate_url

from krunchr.vendors.rethinkdb import db

from .parser import Parser
from .tasks import get_file, push_data

endpoint = Blueprint('analyse_url', __name__)


@endpoint.route('analyse/', methods=['POST'])
@require('url')
@validate({
    'url': validate_url
})
def analyse_url(url):
  name, ext = os.path.splitext(url)
  parse = Parser(ext=ext[1:])

  response = requests.get(url, stream=True)
  fields = []
  for chunk in response.iter_lines(1024):
    fields = parse(chunk)
    if fields:
      break

  task_id = (get_file.s(url, current_app.config['DISCO_FILES']) |
             push_data.s()).apply_async().task_id
  r.table('jobs').insert({
      'url': url,
      'task_id': task_id,
      'state': 'starting',
      'started_at': r.now()
  }).run(db.conn)
  return json.dumps(fields)
