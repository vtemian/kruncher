import os
import time

import rethinkdb as r
import requests

from krunchr.vendors.celery import celery, db


@celery.task(bind=True)
def get_file(self, url, path):
  name, ext = os.path.splitext(url)
  name = str(int(time.time()))

  path = "%s/%s%s" % (path, name, ext)

  response = requests.get(url)
  with open(path, 'w') as f:
    f.write(response.content)

  r.table('jobs').filter({
      'task_id': self.request.id
  }).update({'state': 'done'}).run(db)
