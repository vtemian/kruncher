import os
import subprocess
from subprocess import Popen

from krunchr.vendors.celery import celery


@celery.task(bind=True)
def execute_async(self, command):
  os.chdir('/opt/krunchr/webapp/map/jobs/')
  print os.getcwd()
  c = Popen(command.split(' '), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  import time
  time.sleep(5)
  print c.communicate()
  print command
