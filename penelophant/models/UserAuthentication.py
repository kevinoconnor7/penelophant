""" User Auth Model """

from penelophant.database import db
from .Model import Model
from .User import User
from penelophant.exceptions import MethodNotAllowed
from penelophant.fields import JSONType

class UserAuthentication(Model):
  """ User Auth data representation """
  user_id = db.Column(db.Integer,
    db.ForeignKey(User.id, onupdate="CASCADE", ondelete="CASCADE"),
    primary_key=True
  )
  provider = db.Column(db.String(120), primary_key=True)
  key = db.Column(db.String(256), primary_key=True)
  provider_details = db.Column(JSONType())

  user = db.relationship(User)

  __api_fields__ = []

  def to_api(self):
    raise MethodNotAllowed()
