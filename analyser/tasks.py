import os
import time

import requests

from krunchr.vendors.celery import celery


@celery.task
def get_file(url, path):
  name, ext = os.path.splitext(url)
  name = str(int(time.time()))

  path = "%s/%s%s" % (path, name, ext)

  response = requests.get(url)
  print path
  with open(path, 'w') as f:
    f.write(response.content)
