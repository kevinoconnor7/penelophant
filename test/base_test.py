import warnings
from flask.ext.testing import TestCase
from penelophant import app
from penelophant.database import db
from penelophant.config.TestingConfig import TestingConfig
from sqlalchemy import exc as sa_exc
# pylint: disable=W0401,W0614
from penelophant.models import *

class BaseTestCase(TestCase):
  """ Base test case for Flask testing """

  def create_app(self):
    app.config.from_object(TestingConfig())
    db.init_app(app)
    return app

  def setUp(self):
    # db.create_all()
    db.metadata.create_all(bind=db.engine)

  def tearDown(self):
    db.metadata.drop_all(bind=db.engine)
