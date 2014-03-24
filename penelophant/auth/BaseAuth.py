""" Base Abstract class for user authentication """
from abc import ABCMeta, abstractmethod

class BaseAuth(object):
  """ Abstract Auth class"""
  __metaclass__ = ABCMeta

  def getUser(self, **kwargs):
    """ Use the given with the key and data to confirm login """
    return None

  @abstractmethod
  def setup(self, **kwrargs):
    """ Given a bunch of information, setup the auth provider for user """
    pass
