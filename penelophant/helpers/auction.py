""" Auction helper functions """
from penelophant.models import Auction
from penelophant.models import auctions

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
