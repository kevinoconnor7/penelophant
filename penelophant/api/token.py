""" User API representation object """

from flask import g
from flask_restful import Resource, abort
from penelophant import auther
from penelophant.auth.utils import generate_user_token

class Token(Resource):
  """ Token API """

  def __init__(self):
    pass

  @auther.login_required
  def get(self):
    """ Return a token for logged in users """
    if not g.user:
      abort(403, message='Not valid login found')
    return {
      "token": generate_user_token(g.user).decode('ascii')
    }, 200
