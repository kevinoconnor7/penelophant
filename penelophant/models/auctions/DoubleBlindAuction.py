""" Double Blind Auction implementation """
from penelophant.models.Auction import Auction

class DoubleBlindAuction(Auction):
  """ Double Blind Auction implementation """

  __type__ = 'doubleblind'
  __name__ = 'Double-Blind Auction'
  __mapper_args__ = {'polymorphic_identity': __type__}

  sealed_bids = True
