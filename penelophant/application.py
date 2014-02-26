""" Application initalizer """

from flask import Flask
from flask_restful import Api
from penelophant.config.DefaultConfig import DefaultConfig
from penelophant import views
from penelophant import api as apis
from .database import db

DEFAULT_APP_NAME = "penelophant"
DEFAULT_MODULES = (
  (views.frontend, ""),
)

def create_app(config=None):
  """ App factory """

  app_name = DEFAULT_APP_NAME

  app = Flask(app_name)

  configure_app(app, config)
  register_modules(app)
  register_api(app)
  register_db(app)

  return app

def configure_app(app, config):
  """ Configuration loader """

  app.config.from_object(DefaultConfig())

  if config is not None:
    app.config.from_object(config)

  app.config.from_envvar('APP_CONFIG', silent=True)

def register_modules(app, modules=None):
  """ Register the view modules """
  if not modules:
    modules = DEFAULT_MODULES
  for module, url_prefix in modules:
    app.register_module(module, url_prefix=url_prefix)

def register_api(app):
  """ Register the API """
  api = Api(app, '/api')
  api.add_resource(apis.User, '/users/<string:user_id>')
  api.add_resource(apis.UserList, '/users')

def register_db(app):
  """ Load SQLAlchemy into the app """
  db.init_app(app)
