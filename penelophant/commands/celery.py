""" Database commands """

from flask_script import Command
from penelophant import app, celery

class CeleryCmd(Command):
  """ DB initializer command """
  def __init__(self):
    pass

  # pylint: disable=E0202
  def run(self):
    """ Execute command """
    celery.config_from_object(app.config)
    with app.app_context():
      # celery.start(argv=['beat','-A penelophant.tasks'])
      celery.start(argv=["celery", "beat", "-A", "penelophant.tasks"])
