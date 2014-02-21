#!/usr/bin/env python

from os import environ
import subprocess

from flask.ext.script import Manager

# initialize app before further imports
from penelophant import app

manager = Manager(app)

if __name__ == '__main__':
    manager.run()
