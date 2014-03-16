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
