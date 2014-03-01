""" PasswordAuth class for password-based user authentication """
from penelophant.auth.BaseAuth import BaseAuth
from penelophant.exceptions import AuthSetupMissingInfo
#pylint: disable=E0611
from passlib.hash import bcrypt_sha256

class PasswordAuth(BaseAuth):
  """ Standard hashed password login """

  provider = "password"

  def handleLogin(self, given, key, data):
    """ Use the given with the key and data to confirm login """
    return False


  def setup(self, **kwargs):
    """ Given a bunch of information, setup the auth provider for user """
    if not getattr(kwargs, 'password'):
      raise AuthSetupMissingInfo("No password provided")

    key = bcrypt_sha256.encrypt(getattr(kwargs, 'password'))
    data = dict()

    return key, data
