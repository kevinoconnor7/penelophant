""" Custom exceptions """

class MethodNotAllowed(Exception):
  """ Calls to this method are not permitted """
  def __init__(self):
    super(MethodNotAllowed, self).__init__()

  def __str__(self):
    return "Access to this method is denied"

class AuthSetupMissingInfo(Exception):
  """ Authentication setup is missing information """
  def __init__(self, s):
    super(AuthSetupMissingInfo, self).__init__()
    self.s = s

  def __str__(self):
    return repr(self.s)

class InvoiceAlreadyPaid(Exception):
  """ The invoice has already been paid """
  def __init__(self):
    super(InvoiceAlreadyPaid, self).__init__()

  def ___str___(self):
    return "Duplicate payments are not permitted"

class AuctionStillLive(Exception):
  """ Auction has not ended """
  def __init__(self):
    super(AuctionStillLive, self).__init__()

  def ___str___(self):
    return "The auction has not ended"

