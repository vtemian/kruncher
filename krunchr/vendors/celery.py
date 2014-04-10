from __future__ import absolute_import

from celery import Celery

from krunchr.app import get_config

celery = Celery('krunchr')

config = get_config()
celery.config_from_object(config)
