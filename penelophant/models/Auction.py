""" Auction Model """

from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import object_session
from penelophant.database import db
from .Model import Model
from .User import User
from .Bid import Bid

class Auction(Model):
  """ Auction data representation """
  id = db.Column(db.Integer, primary_key=True)
  creator_user_id = db.Column(db.Integer,
    db.ForeignKey(User.id, ondelete='RESTRICT', onupdate='CASCADE'),
    nullable=False
  )
  start_time = db.Column(db.TIMESTAMP, default=db.func.now())
  end_time = db.Column(db.TIMESTAMP)

  title = db.Column(db.String(100), nullable=False)

  start_price = db.Column(db.Numeric('13,2'), default=0)
  reserve = db.Column(db.Numeric('13,2'), default=0)

  type = db.Column('type', db.String(50))

  creator = db.relationship(User)

  sealed_bids = False

  # Populated by the backref
  bids = db.relationship(Bid, backref="auction")

  __mapper_args__ = {
    'polymorphic_on': type
  }

  @property
  def reserve_met(self):
    """ Return whether not not the reserve has been met """
    highest_bid = self.get_highest_bid()
    if highest_bid is None:
      return False

    return highest_bid.price >= self.reserve

  @property
  def has_ended(self):
    """ Whether or not the auction has ended """
    return self.end_time < datetime.utcnow()

  @property
  def has_started(self):
    """ Whether or not the auction has started """
    return self.start_time <= datetime.utcnow()

  @property
  def current_price(self):
    """ What the current price is """
    highest_bid = self.get_highest_bid()
    if highest_bid is None:
      return self.start_price

    return highest_bid.price


  @property
  def posted_bids(self):
    """ Get posted bids for the auction """
    if self.sealed_bids:
      return None

    return object_session(self)\
      .query(Bid)\
      .with_parent(self)\
      .order_by(Bid.price.desc())\
      .order_by(Bid.bid_time.desc())\
      .all()

  @property
  def highest_bid(self):
    """ Return the highest bid """
    if self.sealed_bids:
      return None

    return self.get_highest_bid()

  def create_bid(self, bid):
    """ Create bid handler, returns (bid, message). Return None for bid if it shouldn't be made """
    return bid, None

  def find_winner(self):
    """ Determine winner logic and return (winning_bid, invoice_amount) """
    return None, None

  def get_highest_bid(self):
    """ Return the highest bid """
    try:
      return object_session(self)\
        .query(Bid)\
        .with_parent(self)\
        .order_by(Bid.price.desc())\
        .order_by(Bid.bid_time.asc())\
        .one()
    except NoResultFound:
      return None
