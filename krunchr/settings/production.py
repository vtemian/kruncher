from krunchr.settings.base import *


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {},
    'formatters': {
        'syslog': {
            'format': '%(asctime)s ' + HOSTNAME_SHORT +
                      ' %(name)s: %(levelname)s: %(message)s',
            'datefmt': '%b %d %H:%M:%S',
        }
    },
    'handlers': {
        'logfile': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'INFO',
            'formatter': 'syslog',
            'when': 'midnight',
            'backupCount': 5,
            'filename': '/var/log/krunchr/app.log',
        },
        'gunicorn': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'INFO',
            'formatter': 'syslog',
            'when': 'midnight',
            'backupCount': 5,
            'filename': '/var/log/krunchr/gunicorn.log',
        },
        'celery': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'INFO',
            'formatter': 'syslog',
            'when': 'midnight',
            'backupCount': 5,
            'filename': '/var/log/krunchr/celery.log',
        },


    },
    'loggers': {
        'gunicorn.error': {
            'handlers': ['gunicorn'],
        },
        'krunchr': {
            'handlers': ['logfile'],
        },
        'celery.task': {
            'handlers': ['celery'],
            'level': 'INFO'
        },
    },
}
