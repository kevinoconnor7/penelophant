from test.base_test import BaseTestCase
from penelophant.models import User, Auction, Bid, Invoice
from penelophant import crud
from werkzeug.exceptions import NotFound

class InvoiceTest(BaseTestCase):
  def setUp(self):
    super(InvoiceTest, self).setUp()

    self.u = User()
    self.u.email = "InvoiceTest@InvoiceTest.tld"
    self.u.display_name = "InvoiceTest"

    crud.add(self.u)

    user2 = User()
    user2.email = "InvoiceTest2@InvoiceTest2.tld"
    user2.display_name = "InvoiceTest2"

    crud.add(user2)

    self.auction = Auction()
    self.auction.title = "InvoiceTest"
    self.auction.type = "doubleblind"
    self.auction.creator = user2

    crud.add(self.auction)

    self.bid = Bid()
    self.bid.price = 50
    self.bid.user = self.u
    self.bid.auction = self.auction

    crud.add(self.bid)

    self.invoice = Invoice()
    self.invoice.bid = self.bid
    self.invoice.payer = self.u
    self.invoice.payee = user2
    self.invoice.amount = self.bid.price

    crud.add(self.invoice)

  def test_get_invoice_by_id(self):
    from penelophant.helpers.invoice import get_invoice_by_id, get_invoice_by_id_or_abort

    self.assertIsNone(get_invoice_by_id(999))
    self.assertEqual(get_invoice_by_id(self.invoice.id), self.invoice)
    with self.assertRaises(NotFound):
      get_invoice_by_id_or_abort(999)

    self.assertEqual(get_invoice_by_id_or_abort(self.invoice.id), self.invoice)
