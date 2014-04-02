""" Auction REST resources """

from flask_restful import Resource
from penelophant import auther
from penelophant.database import db
from penelophant.models.Invoice import Invoice as Invoice_model

#from flask import g
#from flask_restful import Resource, reqparse
#from decimal import Decimal
#from penelophant import crud, auther"""

class InvoiceList(Resource):
  """ Invoice List REST API """

  @auther.login_required
  def get(self):
    """ List all of the user's invoices """
    session = db.session
    invoices = session.query(Invoice_model).all()

    data = dict()
    data['invoices'] = [invoice.to_api() for invoice in invoices]
    data['length'] = len(invoices)

    return data, 200

  def put(self):
    """ User pays an invoice """
