""" Double Blind Auction implementation """
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import object_session
from datetime import datetime, timedelta
from penelophant.models.Auction import Auction
from penelophant.models.Bid import Bid
from penelophant.exceptions import AuctionStillLive

class DoubleBlindAuction(Auction):
  """ Double Blind Auction implementation """

  __type__ = 'doubleblind'
  __name__ = 'Double-Blind Auction'
  __mapper_args__ = {'polymorphic_identity': __type__}

  sealed_bids = True

  @property
  def current_price(self):
    """ What the current price is """
    return 0

  def create_bid(self, bid):
    """ Create bid handler """
    return bid, None

  def find_winner(self):
    """ Determine winner logic and return (winning_bid, invoice_amount) """
    top2 = None

    if not self.has_ended:
      raise AuctionStillLive

    try:
      top2 = object_session(self)\
        .query(Bid)\
        .with_parent(self)\
        .order_by(Bid.price.desc())\
        .order_by(Bid.bid_time.asc())\
        .limit(2)\
        .all()
    except NoResultFound:
      return None, 0

    if top2 is None or len(top2) < 2:
      return None, 0

    winners = [bid for bid in top2]

    return winners[0], winners[1].price
