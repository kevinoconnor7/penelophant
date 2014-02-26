""" Frontend Views """

from flask import Module

frontend = Module(__name__)

@frontend.route('/')
def index():
  """ Place holder index page """
  return "Hello World!"
