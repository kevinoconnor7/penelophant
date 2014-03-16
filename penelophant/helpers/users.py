""" User helpers """

from penelophant.database import db
from penelophant.models.User import User
from flask_restful import abort

def get_user_by_id_or_abort(user_id):
  """ Attempt to get user by id, or abort if it goes south """
  user_id = int(user_id)
  session = db.session
  user = session.query(User).filter(User.id == user_id).first()
  if not user:
    abort(404, message="User {} doesn't exist".format(user_id))
  return user


def get_user_by_email_or_abort(email):
  """ Attempt to get user by email, or abort if it goes south """
  session = db.session
  user = session.query(User).filter(User.email == email).first()
  if not user:
    abort(404, message="User {} doesn't exist".format(email))
  return user
