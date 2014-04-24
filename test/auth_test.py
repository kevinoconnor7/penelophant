from flask import request
from test.base_test import BaseTestCase
from penelophant.auth.utils import import_module, module_member, load_backends, get_backend, \
  generate_user_token, verify_user_token
from penelophant.auth.httpauth import HTTPAuth
from penelophant.models import User, UserAuthentication
from penelophant.application import verify_token
from penelophant import crud, app

class AuthTest(BaseTestCase):
  def setUp(self):
    super(AuthTest, self).setUp()

    self.u = User()
    self.u.email = "AuthTest@AuthTest.tld"
    self.u.display_name = "AuthTest"

    crud.add(self.u)

  def test_import_module(self):
    module = import_module('penelophant.auth.backends.PasswordAuth')
    self.assertEqual(module.__name__, "penelophant.auth.backends.PasswordAuth")

  def test_module_member(self):
    clz = module_member('penelophant.auth.backends.PasswordAuth.PasswordAuth')
    from penelophant.auth.backends.PasswordAuth import PasswordAuth
    self.assertEqual(clz, PasswordAuth)

  def test_load_backends(self):
    backends = load_backends(('penelophant.auth.backends.PasswordAuth.PasswordAuth',))
    self.assertEqual(len(backends), 1)
    from penelophant.auth.backends.PasswordAuth import PasswordAuth
    self.assertEqual(backends[PasswordAuth.provider], PasswordAuth)

  def test_get_backend(self):
    backends = load_backends(('penelophant.auth.backends.PasswordAuth.PasswordAuth',))
    from penelophant.auth.backends.PasswordAuth import PasswordAuth
    self.assertEqual(get_backend(PasswordAuth.provider), PasswordAuth)

  def test_token(self):
    token = generate_user_token(self.u)
    self.assertIsNotNone(token)

    self.assertEqual(verify_user_token(token), self.u)

  def test_get_token(self):
    h = HTTPAuth()
    token = "test"
    with app.test_request_context('/', headers={'authorization': 'Bearer %s' % (token)}) as c:
      self.assertEqual(token, h.get_token())

  def test_login_required(self):
    h = HTTPAuth()
    h.get_verify_token_callback = verify_token
    self.assertEqual(h.login_required(lambda x: x)(1).status_code, 401)

    token = generate_user_token(self.u)
    with app.test_request_context('/', headers={'authorization': 'Bearer %s' % (token)}) as c:
      self.assertEqual(h.login_required(lambda x: x)(1),1)

  def test_error_handler(self):
    h = HTTPAuth()
    r = h.auth_error_callback()
    self.assertEqual(r.status_code, 401)

  def test_pwd_auth(self):
    from penelophant.auth.backends.PasswordAuth import PasswordAuth
    p = PasswordAuth()
    password = 'test123'
    self.assertEqual(p.provider, 'password')
    ua = UserAuthentication()
    ua.user = self.u
    ua.provider = p.provider

    key, details = p.setup(password)
    self.assertIsNotNone(key)
    self.assertIsNotNone(details)

    ua.key = key
    ua.provider_details = details

    crud.add(ua)

    self.assertEqual(p.getUser(self.u.email, password), self.u)

