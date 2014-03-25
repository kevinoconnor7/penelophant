""" Provide HTTP based authentication """

from functools import wraps
from flask import request, make_response
from base64 import b64decode


class HTTPAuth(object):
  """ HTTP Bases authentication using authorization token """

  def __init__(self):
    def default_auth_error():
      """ Return auth error message """
      return "Unauthorized Access"

    self.auth_error_callback = None
    self.get_verify_token_callback = None
    self.error_handler(default_auth_error)


  def error_handler(self, f):
    """ Set the default handler for auth errors """
    @wraps(f)
    def decorated(*args, **kwargs):
      """ Ensure that a 401 error is returned """
      res = f(*args, **kwargs)
      if type(res) == str:
        res = make_response(res)
        res.status_code = 401
      return res
    self.auth_error_callback = decorated
    return decorated

  def login_required(self, f):
    """ Require authentication for a given endpoint """

    @wraps(f)
    def decorated(*args, **kwargs):
      """ Require auth or throw error """
      auth = request.headers.get('authorization')
      if auth:
        auth = auth.split()

        if len(auth) != 2 or auth[0] != 'Bearer' or not auth[1]:
          token = None
        else:
          token = b64decode(auth[1])
      else:
        token = None

      if not self.authenticate(token):
        return self.auth_error_callback()
      return f(*args, **kwargs)
    return decorated

  def verify_token(self, f):
    """ Set the token verification callback function """
    self.get_verify_token_callback = f
    return f

  def authenticate(self, token):
    """ Handle token authentication """
    return self.get_verify_token_callback(token)
