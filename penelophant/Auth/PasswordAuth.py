""" PasswordAuth class for password-based user authentication """
from .BaseAuth import BaseAuth
from penelophant.models.User import User
from rom.columns import String

class PasswordAuth(BaseAuth):

  def __init__(self):
    User.salt = String()
    USer.hash = String()

  def handleLogin(self):
    pass
