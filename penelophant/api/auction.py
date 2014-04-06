""" Auction REST resources """

from flask import g, Markup
from flask_restful import Resource, reqparse, abort, fields, marshal
from decimal import Decimal
from datetime import datetime, timedelta
from penelophant import crud, auther
from penelophant.database import db
from penelophant.helpers.auction import find_auction_type
from penelophant.models.Auction import Auction as Auction_model

auction_fields = {
  'id': fields.Integer,
  'title': fields.String,
  'type': fields.String,
  'reserve_met': fields.Boolean,
  'sealed_bids': fields.Boolean,
  'start_time': fields.DateTime,
  'end_time': fields.DateTime,
  'highest_bid': fields.Nested({
    'id': fields.Integer,
    'price': fields.Fixed(decimals=2)
  }),
  'creator': fields.Nested({
    'id': fields.Integer,
    'display_name': fields.String
  }),
  'bids': fields.List(fields.Nested({
    'price': fields.Fixed(decimals=2),
    'bid_time': fields.DateTime
  })),
  'has_started': fields.Boolean,
  'has_ended': fields.Boolean,
  'current_price': fields.Fixed(decimals=2)
}

class AuctionList(Resource):
  """ Auction List REST API """

  def get(self):
    """ List all auctions """
    session = db.session
    auctions = session.query(Auction_model)\
      .filter(Auction_model.start_time <= datetime.utcnow())\
      .filter(Auction_model.end_time > datetime.utcnow())

    parser = reqparse.RequestParser()
    parser.add_argument('query', type=str)
    args = parser.parse_args()

    if args.query is not None and args.query:
      auctions.filter(Auction_model.title.like(args.query))

    auctions = auctions.all()

    return marshal(auctions, auction_fields), 200

  @auther.login_required
  def post(self):
    """ Handle auction creation """
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str)
    parser.add_argument('type', type=str)
    parser.add_argument('start_time', type=int) # Must be a UNIX timestamp
    parser.add_argument('end_time', type=int) # Must be a UNIX timestamp
    parser.add_argument('reserve', type=Decimal)
    parser.add_argument('start_price', type=Decimal)

    args = parser.parse_args()

    start_time = datetime.utcnow()
    if args.start_time:
      start_time = datetime.utcfromtimestamp(args.start_time)
    end_time = datetime.utcfromtimestamp(args.end_time)

    if args.title is None:
      abort(400, message="You need a title for this auction!")

    if args.type is None:
      abort(400, message="You need a type for this auction!")

    if not end_time > start_time:
      abort(400, message="End time cannot before the start time")

    if not start_time >= datetime.utcnow()-timedelta(seconds=30):
      abort(400, message="Start time cannot be in the past")

    if args.start_price is None:
      args.start_price = 0

    if args.reserve is None:
      args.reserve = 0

    if args.reserve < 0:
      abort(400, message="Reserve price must be positive")

    if args.start_price < 0:
      abort(400, message="Start price must be positive")

    if args.start_price > args.reserve:
      args.reserve = 0

    auction = find_auction_type(args.type)()
    auction.title = Markup.escape(args.title)
    auction.start_time = start_time
    auction.end_time = end_time
    auction.reserve = args.reserve
    auction.start_price = args.start_price
    auction.creator = g.user

    crud.add(auction)

    return marshal(auction, auction_fields), 201

class Auction(Resource):
  """ Auction REST API Endpoint """

  def get(self, auction_id):
    """ Retrieve a specific auction """
    session = db.session
    auction = session.query(Auction_model).get(auction_id)

    if auction.start_time > datetime.utcnow() and auction.creator != g.user:
      abort(403, message="Not authorized to view this auction")

    return marshal(auction, auction_fields), 200

  #pylint: disable=R0915
  @auther.login_required
  def put(self, auction_id):
    """ Update an auction """

    session = db.session
    auction = session.query(Auction_model).get(auction_id)

    if auction.creator != g.user:
      abort(403, message="Not authorized to update auction")

    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str)
    parser.add_argument('reserve', type=Decimal)
    parser.add_argument('start_time', type=int) # Must be a UNIX timestamp
    parser.add_argument('end_time', type=int) # Must be a UNIX timestamp
    parser.add_argument('start_price', type=Decimal)

    args = parser.parse_args()

    if not args.start_time:
      start_time = auction.start_time
    else:
      start_time = datetime.utcfromtimestamp(args.start_time)

    if not args.end_time:
      end_time = auction.end_time
    else:
      end_time = datetime.utcfromtimestamp(args.end_time)

    if args.title is None:
      args.title = auction.title

    if args.reserve is None:
      args.reserve = auction.reserve

    if args.start_price is None:
      args.start_price = auction.start_price

    if not end_time > start_time:
      abort(400, message="End time cannot before the start time")

    if args.start_price is None:
      args.start_price = 0

    if args.reserve is None:
      args.reserve = 0

    if args.reserve < 0:
      abort(400, message="Reserve price must be positive")

    if args.start_price < 0:
      abort(400, message="Start price must be positive")

    # Auction has started
    if datetime.utcnow() >= auction.start_time:
      if args.reserve > auction.reserve:
        abort(400, message="Reserve cannot be increased once the auction has started")

      if args.start_price != auction.start_price:
        abort(400, message="Starting price cannot be changed once the auction has started")

      if start_time != auction.start_time:
        abort(400, message="Start time cannot be changed once the auction has started")

      if end_time != auction.end_time:
        abort(400, message="End time cannot be changed once the auction has started")
    else:
      if not start_time >= datetime.utcnow()-timedelta(seconds=30):
        abort(400, message="Start time cannot be in the past")

    auction.title = Markup.escape(args.title)
    auction.start_time = start_time
    auction.end_time = end_time
    auction.reserve = args.reserve
    auction.start_price = args.start_price

    crud.save()

    return marshal(auction, auction_fields), 200
