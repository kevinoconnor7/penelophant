""" Frontend Views """

from flask import Module
from penelophant import app

frontend = Module(__name__)

@frontend.route('/')
def index():
  """ Serve index page """
  return app.send_static_file('index.html')


@frontend.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)
