""" User API representation object """

from flask_restful import Resource
#from penelophant.auth.utils import get_backend

class Auth(Resource):
  """ Authentication API """

  def __init__(self):
    pass

  def post(self):
    """ Attempt login """
    pass
