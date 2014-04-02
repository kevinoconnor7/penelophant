""" Bid Model """

from penelophant.database import db
from .Model import Model
from .User import User

class Bid(Model):
  """ Bid data representation """
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

  user = db.relationship(User)

  # Will be populated by backref
  auction = None

  __api_fields__ = [
    'id',
    'user',
    'auction',
    'bid_time',
    'price'
  ]
