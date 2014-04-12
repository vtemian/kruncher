from socket import gethostname

HOSTNAME = gethostname()
HOSTNAME_SHORT = HOSTNAME.split('.')[0]

APPLICATION_ROOT = '/v1/krunchr'

DEBUG = True

RETHINKDB_HOST = 'batman.krunchr.net'
RETHINKDB_PORT = 28019
RETHINKDB_AUTH = ''
RETHINKDB_DB = 'krunchr'

BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'

# we must use a safe serializer in order to run celery as root
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERYD_HIJACK_ROOT_LOGGER = False

CELERY_IMPORTS = ('analyser.tasks', 'map.jobs.sum', 'utils.tasks.execute')

DISCO_FILES = '/tmp'
DISCO_NODES = '3'
