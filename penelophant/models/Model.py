""" Base Model with JSON Serialization """
from penelophant.database import db
import datetime
import json

class Model(db.Model):
  """ Abstract Base Model """
  __abstract__ = True
  __api_fields__ = None

  def __init__(self, **kwargs):
    pass

  def __repr__(self):
    if 'id' in self.__table__.columns.keys():
      return '%s(%s)' % (self.__class__.__name__, self.id)
    data = {}
    for key in self.__table__.columns.keys():
      val = getattr(self, key)
      if type(val) is datetime:
        val = val.strftime('%Y-%m-%dT%H:%M:%SZ')
      data[key] = val
    return json.dumps(data, use_decimal=True)
