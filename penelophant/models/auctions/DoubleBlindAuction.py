""" Double Blind Auction implementation """
from penelophant.models.Auction import Auction

class DoubleBlindAuction(Auction):
  """ Double Blind Auction implementation """
  __mapper_args__ = {'polymorphic_identity': 'doubleblind'}
