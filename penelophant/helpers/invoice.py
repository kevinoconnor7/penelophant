""" Invoice helpers """

from penelophant.database import db
from penelophant.models.Invoice import Invoice
from flask_restful import abort

def get_invoice_by_id(invoice_id):
  """ Get an invoice by its id """
  invoice_id = int(invoice_id)
  session = db.session
  invoice = session.query(Invoice).get(invoice_id)
  return invoice

def get_invoice_by_id_or_abort(invoice_id):
  """ Attempt to get invoice by id, or abort if it goes south-east """
  invoice = get_invoice_by_id(invoice_id)
  if not invoice:
    abort(404, message="Invoice {} doesn't exist".format(invoice_id))
  return invoice
