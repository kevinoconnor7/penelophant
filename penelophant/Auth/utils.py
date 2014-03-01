""" Utility function for authentication """
from penelophant.auth.BaseAuth import BaseAuth
import sys

BACKENDSCACHE = {}

def import_module(name):
  """ Import a given module path """
  __import__(name)
  return sys.modules[name]


def module_member(name):
  """ Split the module and member from path """
  mod, member = name.rsplit('.', 1)
  module = import_module(mod)
  return getattr(module, member)

def load_backends(backends, force=False):
  """ Load backends into cache """
  #pylint: disable=W0603
  global BACKENDSCACHE

  if force:
    BACKENDSCACHE = {}

  if not BACKENDSCACHE:
    for backend in backends:
      b = module_member(backend)
      if issubclass(b, BaseAuth):
        BACKENDSCACHE[b.provider] = b
  return BACKENDSCACHE

def get_backend(backend):
  """ Get a given backend """
  if BACKENDSCACHE.getattr('backend') is not None:
    return BACKENDSCACHE.getattr('backend')
  else:
    return None
