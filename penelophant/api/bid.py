""" Bid REST Endpoints """

from decimal import Decimal
from flask import g
from flask_restful import Resource, abort, reqparse, fields, marshal
from penelophant import crud, auther
from penelophant.models.Bid import Bid as Bid_model
from penelophant.helpers.auction import get_auction_by_id_or_abort

class BidAuction(Resource):
  """ Auction-Bid REST API interaction """

  def get(self, auction_id):
    """ Get the bids for a given auction """
    auction = get_auction_by_id_or_abort(auction_id)

    bids = auction.posted_bids

    data = {'bids': [], 'length': 0}

    if bids is not None:
      data['bids'] = bids
      data['length'] = len(bids)

    ret_fields = {
      'length': fields.Integer,
      'bids': fields.List(fields.Nested({
        'id': fields.Integer,
        'auction': fields.Nested({
          'id': fields.Integer,
          'tite': fields.String
        }),
        'bid_time': fields.DateTime,
        'price': fields.Fixed(decimals=2)
      }))
    }

    return marshal(data, ret_fields), 200

  @auther.login_required
  def post(self, auction_id):
    """ Post a bid to an auction """
    auction = get_auction_by_id_or_abort(auction_id)

    if auction.creator == g.user:
      abort(400, message='Auction owners cannot bid on their own auctions')

    if auction.has_ended:
      abort(400, message='Auction has not started')

    if not auction.has_started:
      abort(404, message='Auction not found')

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=Decimal, help="Bid must be of decimal type")
    args = parser.parse_args()

    if args.price is None or args.price <= 0:
      abort(400, message='Bid price must be positive')

    bid = Bid_model()
    bid.price = args.price
    bid.user = g.user
    bid.auction = auction

    fixed_bid, msg = auction.create_bid(bid)

    if fixed_bid is None:
      abort(400, message=msg)

    crud.add(fixed_bid)

    ret_fields = {
      'id': fields.Integer,
      'auction': fields.Nested({
        'id': fields.Integer,
        'tite': fields.String
      }),
      'bid_time': fields.DateTime,
      'price': fields.Fixed(decimals=2)
    }

    return marshal(fixed_bid, ret_fields), 200
