""" Env Config """

import os
from .DefaultConfig import DefaultConfig

class EnvConfig(DefaultConfig):
  """ Encapsulated configuration settings """
  DEBUG = os.environ.get('PENELOPHANT_DEBUG', False)
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
  SECRET_KEY = os.environ.get('PENELOPHANT_SECRET_KEY')
  AUTH_BACKENDS = []
  if os.environ.get('PENELOPHANT_AUTH_BACKENDS'):
    AUTH_BACKENDS = os.environ.get('PENELOPHANT_AUTH_BACKENDS').split(',')
