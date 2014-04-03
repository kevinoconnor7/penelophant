""" Faker commands """

from datetime import datetime, timedelta
from flask_script import Command
# pylint: disable=W0401,W0614
from penelophant.models import *
from penelophant import crud
from random import randint


class Fake(Command):
  """ Fake input data command """
  f = None

  def __init__(self):
    pass

  # pylint: disable=E0202
  def run(self):
    """ Execute command """
    from faker import Factory
    from penelophant.fakers.products import Provider as ProductProvider

    self.f = Factory.create('en_US')
    self.f.add_provider(ProductProvider)

    n = 20 # number of users/auctions

    users = [] # list of users
    auctions = [] # list of auctions
    bids = [] # list of bids

    for i in range(n):
      user = User()
      profile = self.f.simple_profile()
      user.email = profile['mail']
      user.display_name = profile['username']
      crud.add(user)
      users.append(user)

    for i in range(n):
      start_price = randint(0, 150)
      auction = Auction()
      auction.title = self.f.product()
      auction.creator = users[randint(1, len(users))-1]
      auction.end_time = datetime.utcnow() + timedelta(minutes=randint(20, 14400))
      auction.start_price = start_price
      auction.reserve = start_price+randint(0, 50)
      auction.type = 'doubleblind'
      crud.add(auction)
      auctions.append(auction)

    for i in range(len(auctions)):
      last_price = auctions[i].start_price
      last_user = None
      for dummy in range(randint(0, 5)):
        user = users[randint(1, len(users))-1]
        while user == auctions[i] and user != last_user:
          user = users[randint(1, len(users))-1]

        last_user = user
        bid = Bid()
        bid.user = user
        bid.auction = auctions[i]
        bid.price = last_price+randint(1, 50)
        crud.add(bid)
        bids.append(bid)

