""" User API representation object """

from flask import g
from flask_restful import Resource, abort, reqparse, fields, marshal
from penelophant import auther
from penelophant.auth.utils import get_backend
from penelophant.models.UserAuthentication import UserAuthentication
from penelophant.auth.utils import generate_user_token
from penelophant.exceptions import AuthSetupMissingInfo

from penelophant import crud
from sqlalchemy.exc import IntegrityError

class Auth(Resource):
  """ Authentication API """

  def __init__(self):
    pass

  def post(self, provider):
    """ Attempt login """
    backend = self.get_backend(provider)()

    parser = reqparse.RequestParser()
    for f in backend.loginFields:
      parser.add_argument(f[0], type=f[1])

    args = parser.parse_args()

    user = backend.getUser(**args)
    if not user:
      abort(403, message='Login failed')
    else:
      # session['user_id'] = user.id
      data = {'user': user, 'token': generate_user_token(user)}
      ret_fields = {
        'token': fields.String,
        'user': fields.Nested({
          'id': fields.Integer,
          'email': fields.String
        })
      }
      return marshal(data, ret_fields), 200

  @auther.login_required
  def put(self, provider):
    """ Create auth details for a provider """
    backend = self.get_backend(provider)

    parser = reqparse.RequestParser()
    for f in backend.setupFields:
      parser.add_argument(f[0], type=f[1])

    args = parser.parse_args()

    try:
      key, details = backend().setup(**args)
    except AuthSetupMissingInfo:
      abort(400, message="Missing data for auth provider")

    ua = UserAuthentication()
    ua.user = g.user
    ua.provider = backend.provider
    ua.key = key
    ua.provider_details = details

    try:
      crud.add(ua)
    except IntegrityError:
      abort(400, message="Authentication provider and details already exist")

    return '', 201

  def get_backend(self, provider):
    """ Get auth backend """
    backend = get_backend(provider)
    if not backend:
      abort(404, message='Unknown provider')
    return backend


