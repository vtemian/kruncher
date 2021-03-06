import logging
import os
from importlib import import_module

from raven.contrib.flask import Sentry
from raven.middleware import Sentry as SentryMiddleware

from flask import Flask, url_for

from krunchr.vendors.rethinkdb import db

ENDPOINTS = ['analyser', 'crunch']
cache = []


def get_config():
  env_config = os.getenv('KRUNCHR_SETTINGS_MODULE',
                         'krunchr.settings.production')
  return import_module(env_config)


def create_app(config=None):
  app = Flask(__name__)

  config = get_config()
  app.config.from_object(config)

  db.init_app(app)

  app = register_endpoints(app)

  @app.errorhandler(404)
  def page_not_found(e):
    import urllib
    output = ""
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        line = "<strong>%s</strong> %s %s" % (rule.endpoint, methods, urllib.unquote(url))
        output += "<li>" + line + "</li>"

    return """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.</p>

<h3>Current routes:</h3>
<ul>
%s
</ul>
    """ % output, 404

  if 'LOGGING' in app.config:
    configure_logging(app.config['LOGGING'])

  if 'SENTRY_DSN' in app.config:
    sentry = Sentry(dsn=app.config['SENTRY_DSN'], logging=True,
                    level=logging.ERROR)
    sentry.init_app(app)
    app.wsgi = SentryMiddleware(app.wsgi_app, sentry.client)

  return app


def configure_logging(config):
  import logging.config
  logging.config.dictConfig(config)


def register_endpoints(app):

  for module in ENDPOINTS:
    module = import_module('%s.api' % module)

    app.register_blueprint(module.endpoint, url_prefix='/v1/')

  return app
