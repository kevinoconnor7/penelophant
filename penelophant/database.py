""" Database Module """

from flask_sqlalchemy import SQLAlchemy
from penelophant import app
db = SQLAlchemy(app)
