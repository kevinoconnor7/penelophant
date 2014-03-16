""" Custom DB field types """

from sqlalchemy.types import PickleType, Text
import json

#pylint: disable=W0223
class JSONType(PickleType):
  """ JSON data representation type """
  impl = Text

  def __init__(self, *args, **kwargs):
    kwargs['pickler'] = json
    super(JSONType, self).__init__(*args, **kwargs)
