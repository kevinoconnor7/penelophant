""" Base Model with JSON Serialization """
from penelophant.database import db
import datetime
import json

class Model(db.Model):
  """ Abstract Base Model """
  __abstract__ = True
  _overwrite_columns = True
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

  def to_dict(self, show=None, hide=None, path=None):
    """ Convert model to dict """
    if not show:
      show = []
    if not hide:
      hide = []

    data = {}
    if not path:
      path = self.__tablename__.lower()
      def prepend_path(item):
        """ Follow dot path through Models """
        item = item.lower()
        if item.split('.', 1)[0] == path:
          return item
        if len(item) == 0:
          return item
        if item[0] != '.':
          item = '.%s' % item
        item = '%s%s' % (path, item)
        return item
      show[:] = [prepend_path(x) for x in show]
      hide[:] = [prepend_path(x) for x in hide]

    for key in self.__table__.columns.keys():
      check = '%s.%s' % (path, key)
      if check not in hide and (key is 'id' or check in show):
        data[key] = getattr(self, key)

    for key in self.__mapper__.relationships.keys():
      check = '%s.%s' % (path, key)
      if check not in hide and check in show:
        hide.append(check)
        if self.__mapper__.relationships[key].uselist:
          data[key] = []
          for item in getattr(self, key):
            data[key].append(item.to_dict(
              show=list(show),
              hide=list(hide),
              path=('%s.%s' % (path, key.lower())),
            ))
        else:
          data[key] = getattr(self, key)
          if hasattr(data[key], 'to_api'):
            data[key] = data[key].to_api()

    return data

  def to_api(self):
    """ Return data for API """
    return self.to_dict(show=self.__api_fields__)
