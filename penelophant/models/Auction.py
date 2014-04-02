""" Auction Model """

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
    return False


  __api_fields__ = [
    'id',
    'creator',
    'type',
    #'start_time',
    #'end_time',
    'reserve_met',
    'title',
    'sealed_bids',
    'highest_bid'
  ]

  def create_bid(self, bid):
    """ Create bid logic """
    pass

  def find_winner(self):
    """ Determine winner logic """
    pass

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
    try:
      return object_session(self).query(Bid).with_parent(self).order_by(Bid.price.desc()).one()
    except NoResultFound:
      return None
