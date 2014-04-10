#!/usr/bin/env python
from flask.ext.script import Manager

from krunchr import create_app


if __name__ == "__main__":
  manager = Manager(create_app)

  manager.add_option('-c', '--config', dest='config', required=False)

  manager.run()
