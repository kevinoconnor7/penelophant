""" Auction REST resources """

from flask import g
from flask_restful import Resource, reqparse
from decimal import Decimal
from penelophant import crud, auther
from penelophant.database import db
from penelophant.helpers.auction import find_auction_type
from penelophant.models.Auction import Auction as Auction_model

class AuctionList(Resource):
  """ Auction List REST API """

  def get(self):
    """ List all auctions """
    session = db.session
    auctions = session.query(Auction_model).all()

    data = dict()
    data['auctions'] = [auction.to_api() for auction in auctions]
    data['length'] = len(auctions)

    return data, 200

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

    auction = find_auction_type(args.type)()
    auction.title = args.title
    auction.start_time = args.start_time
    auction.end_time = args.end_time
    auction.reserve = args.reserve
    auction.start_price = args.start_price
    auction.creator = g.user

    crud.add(auction)

    return auction.to_api(), 201
