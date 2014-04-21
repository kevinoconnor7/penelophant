""" Auction REST resources """

from flask import g
from flask_restful import Resource, fields, marshal, reqparse
from penelophant import app, auther, crud
from penelophant.helpers.invoice import get_invoice_by_id_or_abort
from penelophant.exceptions import InvoiceAlreadyPaid
import balanced

invoice_fields = {
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
  'payer': fields.Nested({
      'id': fields.Integer,
      'display_name': fields.String
    }),
  'payee': fields.Nested({
      'id': fields.Integer,
      'display_name': fields.String
    }),
  'paid': fields.Boolean
}

class InvoiceList(Resource):
  """ Invoice List REST API endpoint """

  @auther.login_required
  def get(self):
    """ List all of the user's invoices """
    invoices = g.user.invoices

    return marshal(invoices, invoice_fields), 200

class Invoice(Resource):
  """ Invoice REST API endpoint """

  @auther.login_required
  def get(self, invoice_id):
    """ View a specific invoice """
    invoice = get_invoice_by_id_or_abort(invoice_id)

    return marshal(invoice, invoice_fields), 200

  @auther.login_required
  def put(self, invoice_id):
    """ User pays an invoice """

    parser = reqparse.RequestParser()
    parser.add_argument('ccId', type=str, required=True, location='args')
    args = parser.parse_args()

    invoice = get_invoice_by_id_or_abort(invoice_id)

    if invoice.paid:
      raise InvoiceAlreadyPaid

    print(args)

    card = balanced.Card.fetch('/cards/%s' % args.ccId)
    debit = card.debit(
      appears_on_statement_as=app.config['STATEMENT_MSG'],
      amount=int(invoice.amount*100),
      description="Invoice for invoice #%s" % (invoice.id),
      meta={
        'invoice_id': invoice.id,
        'bid_id': invoice.bid.id,
        'auction_id': invoice.bid.auction.id,
        'payer': invoice.payer.id,
        'payee': invoice.payee.id
      }
    )

    invoice.provider = "balanced"
    invoice.provider_details = debit.id
    invoice.paid = True
    crud.save()

    return marshal(invoice, invoice_fields), 200


