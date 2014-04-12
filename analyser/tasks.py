import os
import time
from shutil import copy2
import subprocess
import time
from subprocess import Popen, PIPE

import rethinkdb as r
import requests
from disco.ddfs import DDFS

from krunchr.vendors.celery import celery, db, config

from .parser import Parser


@celery.task(bind=True)
def get_fields(self, url, ds_id):
  name, ext = os.path.splitext(url)
  parse = Parser(ext=ext[1:])

  response = requests.get(url, stream=True)
  fields = []
  for chunk in response.iter_lines(1024):
    fields = parse(chunk)
    if fields:
      break

  r.table('datasets').filter({
      'id': ds_id,
  }).update({
      'fields': fields,
      'format': parse.format,
      'state': 'download_file',
      'ready': True
  }).run(db)

  return {
      'url': url,
      'ds_id': ds_id
  }


@celery.task(bind=True)
def get_file(self, args, path):
  url = args['url']
  ds_id = args['ds_id']
  name, ext = os.path.splitext(url)
  name = str(int(time.time()))

  path = "%s/%s%s" % (path, name, ext)

  response = requests.get(url)
  with open(path, 'w') as f:
    f.write(response.content)

  r.table('datasets').filter({
      'id': ds_id,
  }).update({
      'state': 'push_data'
  }).run(db)

  return {
      'path': path,
      'ds_id': ds_id,
  }


@celery.task(bind=True)
def push_data(self, args):
  path = args['path']
  ds_id = args['ds_id']

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
  command = 'ddfs push data:%s ./xa?' % ds_id
  d = DDFS('disco://localhost')
  files = [("%s/%s/%s" % (config.DISCO_FILES, tmp_dir, filename), filename) for filename in os.listdir(".") if filename.startswith("xa")]
  d.push('data:%s' % ds_id, files)

  r.table('datasets').filter({
      'id': ds_id,
  }).update({
      'state': 'ready_for_crunching'
  }).run(db)
