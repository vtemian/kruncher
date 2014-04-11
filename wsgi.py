from krunchr.app import create_app
from werkzeug.contrib.fixers import ProxyFix

application = create_app()
application.wsgi_app = ProxyFix(application.wsgi_app)
