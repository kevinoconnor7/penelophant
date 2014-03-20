""" Base Abstract class for user authentication """
from abc import ABCMeta, abstractmethod

class BaseAuth(object):
  """ Abstract Auth class"""
  __metaclass__ = ABCMeta

  def handleLogin(self, given, key, data):
    """ Use the given with the key and data to confirm login """
    return False

  @abstractmethod
  def setup(self, **kwrargs):
    """ Given a bunch of information, setup the auth provider for user """
    pass
