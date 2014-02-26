""" CRUD DB helpers """

from flask import g
from .database import db

def add(obj):
  """ Add object to database """

  g.session = db.session
  g.session.add(obj)
  g.session.flush()
  g.session.commit()

def save():
  """ Save object to database """

  g.session = db.session
  g.session.flush()
  g.session.commit()

def delete(obj):
  """ Delete object from database """

  g.session = db.session
  g.session.delete(obj)
  g.session.flush()
  g.session.commit()
