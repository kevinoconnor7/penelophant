""" Bid REST Endpoints """

from decimal import Decimal
from flask import g
from flask_restful import Resource, abort, reqparse
from penelophant import crud, auther
from penelophant.models.Bid import Bid as Bid_model
from penelophant.helpers.auction import get_auction_by_id_or_abort
#from penelophant.models.Bid import Auction as Auction_model

class BidAuction(Resource):
  """ Auction-Bid REST API interaction """

  def get(self, auction_id):
    """ Get the bids for a given auction """
    auction = get_auction_by_id_or_abort(auction_id)

    bids = auction.posted_bids

    if bids is None:
      return {'bids': {}, 'length': 0}, 200

    data = {
      "bids": [bid.to_api() for bid in bids],
      "length": len(bids)
    }

    return data, 200

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
    parser.add_argument('price', type=Decimal)
    args = parser.parse_args()

    if args.price is None or args.price < 0:
      abort(400, message='Bid price must be positive')

    bid = Bid_model()
    bid.price = args.price
    bid.user = g.user
    bid.auction = auction

    fixed_bid, msg = auction.create_bid(bid)

    if fixed_bid is None:
      abort(400, message=msg)

    crud.add(fixed_bid)

    return fixed_bid.to_api(), 200
