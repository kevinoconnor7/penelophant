""" Faker commands """

from datetime import datetime, timedelta
from flask_script import Command
# pylint: disable=W0401,W0614
from penelophant.models import *
from penelophant import crud
from faker import Factory

class Fake(Command):
  """ Fake input data command """
  def __init__(self):
    pass

  # pylint: disable=E0202
  def run(self):
    """ Execute command """
    f = Factory.create()

    n = 20 # number of users/auctions

    u = [] # list of users
    a = [] # list of auctions
    b = [] # list of bids

    for i in range(n):
      u.append(User(email=f.email(),
                    display_name=f.userName()
                    ))
      crud.add(u[i])
      a.append(Auction(title=f.company(),
                       creator_user_id=u[i].id,
                       end_time=(datetime.utcnow() + timedelta(days=4))
                       ))
      crud.add(a[i])

    for i in range(n, -1, -1):
      b.append(Bid(user_id=u[n-i].id,
                   auction_id=a[i],
                   ))
      crud.add(b[i])

