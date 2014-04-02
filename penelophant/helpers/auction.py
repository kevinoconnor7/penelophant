""" Auction helper functions """
from penelophant.models import Auction
from penelophant.models import auctions
from penelophant.database import db
from penelophant.models.Auction import Auction
from flask_restful import abort

def find_subclasses(module, clazz):
  """ Return all the classes in a given module """
  for name in dir(module):
    o = getattr(module, name)
    try:
      if (o != clazz) and issubclass(o, clazz):
        yield name, o
    except TypeError:
      pass

def find_auction_type(typename):
  """ Return the proper concrete class for an auction type """
  for dummy, clazz in find_subclasses(auctions, Auction):
    if clazz.__type__ == typename:
      return clazz
  return None

def get_auction_by_id(auction_id):
  """ Get a auction by a given id """
  auction_id = int(auction_id)
  session = db.session
  auction = session.query(Auction).get(auction_id)
  return auction

def get_auction_by_id_or_abort(auction_id):
  """ Attempt to get auction by id, or abort if it goes south """
  auction = get_auction_by_id(auction_id)
  if not auction:
    abort(404, message="Auction {} doesn't exist".format(auction))
  return auction
