""" Bid Model """

from penelophant.database import db
from .Model import Model
from .User import User

class Bid(Model):
  """ Bid data representation """

  __mapper_args__ = {
    'order_by': 'price DESC, bid_time ASC'
  }

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer,
    db.ForeignKey(User.id, ondelete='RESTRICT', onupdate='CASCADE'),
    nullable=False
  )
  auction_id = db.Column(db.Integer,
    db.ForeignKey('auction.id', ondelete='RESTRICT', onupdate='CASCADE'),
    nullable=False
  )
  bid_time = db.Column(db.TIMESTAMP, default=db.func.now())
  price = db.Column(db.Numeric('13,2'), default=0)

  user = db.relationship(User, backref="bids")

  # Will be populated by backref
  auction = None
