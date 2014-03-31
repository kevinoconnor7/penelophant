""" Auction REST resources """

from flask_restful import Resource, reqparse
from decimal import Decimal
from penelophant import crud
from penelophant.helpers.auction import find_auction_type

class AuctionList(Resource):
  """ Auction List REST API """

  #@auther.login_required
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

    auction = find_auction_type(args.type)()
    auction.title = args.title
    auction.start_time = args.start_time
    auction.end_time = args.end_time
    auction.reserve = args.reserve
    auction.start_price = args.start_price

    crud.add(auction)

    return auction.to_api(), 201
