""" Base Abstract class for user authentication """
from abc import ABCMeta, abstractmethod

class BaseAuth(object):
  __metaclass__ = ABCMeta

  @abstractmethod
  def handleLogin(self):
    pass
