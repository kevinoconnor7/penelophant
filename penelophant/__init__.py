""" Penelophant Backend App """

from flask import Flask
from penelophant.auth.httpauth import HTTPAuth

app = Flask("penelophant")
auther = HTTPAuth()

def create_app(config=None):
  """ Create application and setup modules """
  from .application import setup_app

  setup_app(config)


  return app


