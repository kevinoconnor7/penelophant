""" Auction REST resources """

from flask import g
from flask_restful import Resource, fields, marshal
from penelophant import auther, crud
from penelophant.database import db
from penelophant.models.Invoice import Invoice as Invoice_model
from penelophant.helpers.invoice import get_invoice_by_id_or_abort
from penelophant.exceptions import InvoiceAlreadyPaid

class InvoiceList(Resource):
  """ Invoice List REST API endpoint """

  @auther.login_required
  def get(self):
    """ List all of the user's invoices """
    session = db.session
    invoices = g.user.invoices

    data = {'invoices': [], 'length': 0}

    if invoices is not None:
      data['invoices'] = invoices
      data['length'] = len(invoices)

    ret_fields = {
      'length': fields.Integer,
      'invoices': fields.List(fields.Nested({
        'id': fields.Integer,
        'bid': fields.Nested({
          'id': fields.Integer,
          'bid_time': fields.DateTime,
          'price': fields.Fixed(decimals=2),
          'auction': fields.Nested({
            'id': fields.Integer,
            'title': fields.String,
            'type': fields.String
          })
        }),
        'amount': fields.Fixed(decimals=2),
        'paid': fields.Boolean
      }))
    }

    return marshal(data, ret_fields), 200

class Invoice(Resource):
  """ Invoice REST API endpoint """

  @auther.login_required
  def put(self, invoice_id):
    """ User pays an invoice """
    invoice = get_invoice_by_id_or_abort(invoice_id)

    if invoice.paid:
      raise InvoiceAlreadyPaid

    # FIXME: actually process payments
    # currently only marks the invoice as paid

    invoice.paid = True
    crud.save()

    ret_fields = {
      'id': fields.Integer,
      'bid': fields.Nested({
          'id': fields.Integer,
          'bid_time': fields.DateTime,
          'price': fields.Fixed(decimals=2),
          'auction': fields.Nested({
              'id': fields.Integer,
              'title': fields.String,
              'type': fields.String
              })
          }),
      'amount': fields.Fixed(decimals=2),
      'paid': fields.Boolean
    }

    return marshal(invoice, ret_fields), 200


