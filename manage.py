#!/usr/bin/env python

from os import environ
import subprocess
from flask.ext.script import Manager
from penelophant.commands.db import InitDB
from penelophant.commands.fake import Fake
# initialize app before further imports
from penelophant import create_app

manager = Manager(create_app)

if __name__ == '__main__':
  manager.add_option(
    '-c',
    '--config',
    dest="config",
    required=False,
    help="config file"
  )
  manager.add_command("initdb", InitDB())
  manager.add_command("fake", Fake())
  manager.run()
