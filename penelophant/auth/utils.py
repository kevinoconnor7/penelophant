""" Utility function for authentication """
from penelophant.auth.BaseAuth import BaseAuth
from penelophant.helpers.users import get_user_by_id
from penelophant import app
from flask import g
import jwt
from datetime import datetime, timedelta
import sys

BACKENDSCACHE = {}

def import_module(name):
  """ Import a given module path """
  __import__(name)
  return sys.modules[name]


def module_member(name):
  """ Split the module and member from path """
  mod, member = name.rsplit('.', 1)
  module = import_module(mod)
  return getattr(module, member)

def load_backends(backends, force=False):
  """ Load backends into cache """
  #pylint: disable=W0603
  global BACKENDSCACHE

  if force:
    BACKENDSCACHE = {}

  if not BACKENDSCACHE:
    for backend in backends:
      b = module_member(backend)
      if issubclass(b, BaseAuth):
        BACKENDSCACHE[b.provider] = b
  return BACKENDSCACHE

def get_backend(backend):
  """ Get a given backend """
  return BACKENDSCACHE.get(backend, None)

def generate_user_token(user):
  """ Generate a token for a given user """

  return jwt.encode({
    "exp": datetime.utcnow() + timedelta(hours=6),
    "user_id": user.id
  }, app.config['SECRET_KEY'])

def verify_user_token(token):
  """ Verify a user token and return the User who its generated for """
  user = getattr(g, 'user', None)
  if user:
    return user
  try:
    payload = jwt.decode(token, app.config['SECRET_KEY'])
    return get_user_by_id(payload.get('user_id', None))
  except (jwt.DecodeError, jwt.ExpiredSignature):
    return None
