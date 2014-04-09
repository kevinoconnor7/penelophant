""" Auction completion task runner """

from flask import Flask
from datetime import datetime, timedelta
from celery import Celery
from penelophant import crud
from penelophant.database import db
from penelophant.models.Auction import Auction as Auction_model
from penelophant.models.Invoice import Invoice as Invoice_model

def make_celery(app):
  """ Make Celery object

  http://flask.pocoo.org/docs/patterns/celery/
  """
  celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
  celery.conf.update(app.config)
  TaskBase = celery.Task
  # pylint: disable=C0111
  class ContextTask(TaskBase):
    abstract = True
    def __call__(self, *args, **kwargs):
      with app.app_context():
        return TaskBase.__call__(self, *args, **kwargs)
  celery.Task = ContextTask
  return celery

flask_app = Flask(__name__)
flask_app.config.update(
  CELERY_BROKER_URL="memory://",
  CELERY_CACHE_BACKEND="cache://memory",
  CELERYBEAT_SCHEDULE={
    'auction-completion-task-runner': {
      'task': 'tasks.auction_completion',
      'schedule': timedelta(seconds=30)
      },
    }
  )

# pylint: disable=W0621
my_celery = make_celery(flask_app)

@my_celery.task()
def auction_completion():
  """ Check if auction is complete

  If it is, mark it as ended and generate an invoice.
  """
  session = db.session
  auctions = session.query(Auction_model)\
    .filter(Auction_model.end_time < datetime.utcnow())\
    .filter(Auction_model.has_ended == False)

  for auction in auctions:
    auction.has_ended = True

    inv = Invoice_model()
    inv.bid, inv.amount = auction.find_winner()
    inv.user = inv.bid.user

    crud.add(inv)

  return

