""" Auction completion task runner """

from celery.signals import task_postrun
from datetime import datetime
from penelophant import crud, celery
from penelophant.database import db
from penelophant.models.Auction import Auction as Auction_model
from penelophant.models.Invoice import Invoice as Invoice_model

@celery.task()
def auction_completion():
  """ Check if auction is complete

  If it is, generate an invoice.
  """

  session = db.session
  # get all completed auctions
  auctions = session.query(Auction_model)\
   .filter(Auction_model.end_time < datetime.utcnow())

  for auction in auctions:
    inv = Invoice_model()
    inv.bid, inv.amount = auction.find_winner()
    inv.payer = inv.bid.user
    inv.payee = auction.creator

    # add the invoice if it does not exist
    if session.query(Invoice_model).filter(Invoice_model.bid_id == inv.bid_id).count() == 0:
      crud.add(inv)

  return

@task_postrun.connect
def close_session(*args, **kwargs):
  """Flask SQLAlchemy will automatically create new sessions for you from
  a scoped session factory, given that we are maintaining the same app
  context, this ensures tasks have a fresh session (e.g. session errors
  won't propagate across tasks)"""
  db.session.remove()

