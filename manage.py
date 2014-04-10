#!/usr/bin/env python
from flask.ext.script import Manager

from cache_refresh import create_app
from utils.commands import TestCommand


if __name__ == "__main__":
  manager = Manager(create_app)

  manager.add_option('-c', '--config', dest='config', required=False)
  manager.add_command('test', TestCommand(packages=["cache_refresh", "flush"]))

  manager.run()
