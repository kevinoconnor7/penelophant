""" Invoice Model """

from penelophant.database import db
from .Model import Model
from .User import User
from .Bid import Bid
from penelophant.fields import JSONType

class Invoice(Model):
  """ Invoice data representation """
  id = db.Column(db.Integer, primary_key=True)
  payer_user_id = db.Column(db.Integer,
    db.ForeignKey(User.id, ondelete='RESTRICT', onupdate='CASCADE'),
    nullable=False
  )
  payee_user_id = db.Column(db.Integer,
    db.ForeignKey(User.id, ondelete='RESTRICT', onupdate='CASCADE'),
    nullable=False
  )
  bid_id = db.Column(db.Integer,
    db.ForeignKey(Bid.id, ondelete='RESTRICT', onupdate='CASCADE'),
    nullable=False
  )
  amount = db.Column(db.Numeric('13,2'), default=0)
  paid = db.Column(db.Boolean(), default=False)
  provider = db.Column(db.String(120))
  provider_details = db.Column(JSONType())


  payer = db.relationship(User, backref="invoices", foreign_keys=[payer_user_id])
  payee = db.relationship(User, backref="owed_invoices", foreign_keys=[payee_user_id])
  bid = db.relationship(Bid)
