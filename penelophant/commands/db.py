""" Database commands """

from flask_script import Command
from penelophant.database import db
# pylint: disable=W0401,W0614
from penelophant.models import *

class InitDB(Command):
  """ DB initializer command """
  def __init__(self):
    pass

  # pylint: disable=E0202
  def run(self):
    """ Execute command """
    db.metadata.drop_all(bind=db.engine)
    db.metadata.create_all(bind=db.engine)
