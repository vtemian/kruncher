import os
import time
from shutil import copy2
from subprocess import Popen, PIPE

import rethinkdb as r
import requests

from krunchr.vendors.celery import celery, db, config


@celery.task(bind=True)
def get_file(self, url, path, uuid):
  print uuid
  name, ext = os.path.splitext(url)
  name = str(int(time.time()))

  path = "%s/%s%s" % (path, name, ext)

  response = requests.get(url)
  with open(path, 'w') as f:
    f.write(response.content)

  r.table('jobs').filter({
      'task_id': self.request.id
  }).update({
      'state': 'done',
      'finished_at': r.now()
  }).run(db)

  return {
      'path': path,
      'uuid': uuid,
  }


@celery.task(bind=True)
def push_data(self, args):
  path = args['path']
  uuid = args['uuid']

  filename = os.path.basename(path)
  tmp_dir = str(int(time.time()))

  # Create temporary files
  os.chdir(config.DISCO_FILES)
  os.makedirs(tmp_dir)
  copy2(filename, "%s/%s" % (tmp_dir, filename))
  os.chdir(tmp_dir)

  command = 'split -n %s %s' % (config.DISCO_NODES, path)
  split_process = Popen(command.split(' '), stdout=PIPE)
  split_process.communicate()

  # Push data to cluster
  command = 'ddfs push data:%s' % uuid
  push_data = Popen(command.split(' '), stdout=PIPE)
  push_data.communicate()
