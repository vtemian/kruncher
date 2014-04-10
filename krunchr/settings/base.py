from socket import gethostname

HOSTNAME = gethostname()
HOSTNAME_SHORT = HOSTNAME.split('.')[0]

APPLICATION_ROOT = '/v1/krunchr'

DEBUG = False
