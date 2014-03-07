""" User API representation object """

from flask_restful import Resource, abort, reqparse
from penelophant.auth.utils import get_backend
from penelophant.models.UserAuthentication import UserAuthentication
from penelophant.helpers.users import get_user_by_id_or_abort

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
      return user.to_api(), 200

  def put(self, provider):
    """ Create auth details for a provider """
    backend = self.get_backend(provider)

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    for f in backend.setupFields:
      parser.add_argument(f[0], type=f[1])

    args = parser.parse_args()

    user = get_user_by_id_or_abort(args.id)

    key, details = backend().setup(**args)

    ua = UserAuthentication()
    ua.user = user
    ua.provider = backend.provider
    ua.key = key
    ua.provider_details = details

    try:
      crud.add(ua)
    except IntegrityError:
      abort(400, message="Authentication provider and details already exist")

    return '', 200

  def get_backend(self, provider):
    """ Get auth backend """
    backend = get_backend(provider)
    if not backend:
      abort(404, message='Unknown provider')
    return backend


