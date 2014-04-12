import os

from krunchr.vendors.celery import celery


@celery.task(bind=True)
def execute_async(self, command):
  os.system(command)
