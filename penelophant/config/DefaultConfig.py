""" Default Confg """

from datetime import timedelta

class DefaultConfig(object):
  """ Encapsulated configuration settings """
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = None
  SECRET_KEY = "I_AM_SO_SECRET_OMG_OMG_OMG_OMG_123"
  AUTH_BACKENDS = ()
  RSA_KEY = None
  BROKER_URL = "memory://"
  CELERY_CACHE_BACKEND = "cache://memory"
  CELERYBEAT_SCHEDULE = {
    'auction-completion-task-runner': {
      'task': 'tasks.auction_completion',
      'schedule': timedelta(seconds=30)
    },
  }
