""" User Model """

from penelophant.database import db
from .Model import Model

class User(Model):
  """ User data representation """
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True)

  __api_fields__ = [
    'id',
    'email'
  ]
