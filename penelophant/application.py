""" Application initalizer """

from penelophant import app, auther
from flask import g
from flask_restful import Api
from penelophant import views
from penelophant import api as apis
from .database import db
from penelophant.auth.utils import load_backends, verify_user_token
#import balanced <-- httplib doesn't work in python3

DEFAULT_APP_NAME = "penelophant"
DEFAULT_MODULES = (
  (views.frontend, ""),
)

def setup_app(config):
  """ App factory """

  #app_name = DEFAULT_APP_NAME

  #app = Flask(app_name)

  configure_app(config)
  register_modules()
  register_api()
  register_db()
  register_auth_backends()

  #return app

def configure_app(config):
  """ Configuration loader """
  from penelophant.config.DefaultConfig import DefaultConfig

  app.config.from_object(DefaultConfig())

  if config is not None:
    app.config.from_object(config)

  app.config.from_envvar('APP_CONFIG', silent=True)

def register_modules(modules=None):
  """ Register the view modules """
  if not modules:
    modules = DEFAULT_MODULES
  for module, url_prefix in modules:
    app.register_module(module, url_prefix=url_prefix)

def register_api():
  """ Register the API """
  api = Api(app, '/api')

  api.add_resource(apis.User, '/users/<int:user_id>')
  api.add_resource(apis.UserList, '/users')
  api.add_resource(apis.Auth, '/auth/<string:provider>')
  api.add_resource(apis.Token, '/token')

  api.add_resource(apis.AuctionList, '/auctions')
  api.add_resource(apis.Auction, '/auctions/<int:auction_id>')
  api.add_resource(apis.BidAuction, '/auctions/<int:auction_id>/bid')

  api.add_resource(apis.InvoiceList, '/invoices')
  api.add_resource(apis.Invoice, '/invoices/<int:invoice_id>')

def register_db():
  """ Load SQLAlchemy into the app """
  db.init_app(app)

def register_auth_backends():
  """ Register auth backends from config """
  load_backends(app.config['AUTH_BACKENDS'])

@app.before_request
def get_current_user_by_token():
  """ Load the logged in user into a request variable to future use """
  token = auther.get_token()

  user = None

  if token:
    user = verify_user_token(token)

  setattr(g, 'user', user)

@auther.verify_token
def verify_token(token):
  """ Overload the basic auth verify password method """

  user = None

  if token:
    user = verify_user_token(token)

  # For use of session based login
  #if not user:
  #  user = get_user_by_id(session.get('user_id', None))

  if user:
    setattr(g, 'user', user)
    return True
  else:
    return False

