""" Penelophant Backend App """

from flask import Flask
from penelophant.auth.httpauth import HTTPAuth
from celery import Celery

app = Flask("penelophant")
auther = HTTPAuth()
celery = Celery(app.import_name)

def create_app(config=None):
  """ Create application and setup modules """
  from .application import setup_app

  setup_app(config)

  return app


