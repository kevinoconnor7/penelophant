""" PasswordAuth class for password-based user authentication """
from penelophant.auth.BaseAuth import BaseAuth
from penelophant.exceptions import AuthSetupMissingInfo
#pylint: disable=E0611
from passlib.hash import bcrypt_sha256
from penelophant.database import db
from penelophant.models.User import User
from penelophant.models.UserAuthentication import UserAuthentication
from sqlalchemy.orm.exc import NoResultFound


class PasswordAuth(BaseAuth):
  """ Standard hashed password login """

  provider = "password"

  setupFields = [
    ('password', str)
  ]

  loginFields = [
    ('email', str),
    ('password', str)
  ]

  #pylint: disable=W0221
  def getUser(self, email, password):
    """ Given the user's login information, return the user """

    session = db.session
    ua = None
    try:
      ua = session.query(UserAuthentication)\
        .join(User)\
        .filter(UserAuthentication.provider == self.provider)\
        .filter(User.email == email)\
        .one()
    except NoResultFound:
      pass

    if not ua:
      return None

    user = ua.user

    if bcrypt_sha256.verify(password, ua.key):
      return user
    else:
      return None

  def setup(self, password=None, **kwargs):
    """ Given a bunch of information, setup the auth provider for user """
    if not password:
      raise AuthSetupMissingInfo("No password provided")

    key = bcrypt_sha256.encrypt(password)
    data = dict()

    return key, data
