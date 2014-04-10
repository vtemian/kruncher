from __future__ import absolute_import

import rethinkdb as r
from celery import Celery

from krunchr.app import get_config

celery = Celery('krunchr')

config = get_config()
celery.config_from_object(config)

db = r.connect(**{
    'host': config.RETHINKDB_HOST,
    'port': config.RETHINKDB_PORT,
    'auth_key': config.RETHINKDB_AUTH,
    'db': config.RETHINKDB_DB
})
