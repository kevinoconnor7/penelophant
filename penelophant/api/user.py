""" User API representation object """

from flask import g
from sqlalchemy.exc import IntegrityError
from flask_restful import Resource, abort, reqparse, fields, marshal
from penelophant.models.User import User as User_model
from penelophant.database import db
from penelophant import crud, auther
from penelophant.helpers.users import get_user_by_id_or_abort
from penelophant.auth.utils import generate_user_token

class User(Resource):
  """ Specific user API """

  def __init__(self):
    pass

  def get(self, user_id):
    """ Retrieve user """
    user = get_user_by_id_or_abort(user_id)

    ret_fields = {
      'id': fields.Integer,
      'email': fields.String,
      'display_name': fields.String
    }
    return marshal(user, ret_fields), 200

  @auther.login_required
  def delete(self, user_id):
    """ Delete user """
    user = get_user_by_id_or_abort(user_id)

    if user != g.user:
      abort(403, message="Not authorized to delete user")

    crud.delete(user)
    return '', 204

  @auther.login_required
  def put(self, user_id):
    """ Update a user """
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str)
    parser.add_argument('display_name', type=str)
    args = parser.parse_args()

    user = get_user_by_id_or_abort(user_id)

    if user != g.user:
      abort(403, message="Not authorized to update user")

    user.email = args.email
    user.display_name = args.display_name
    crud.save()

    ret_fields = {
      'id': fields.Integer,
      'email': fields.String,
      'display_name': fields.String
    }
    return marshal(user, ret_fields), 200

class UserList(Resource):
  """ User index API """

  def __init__(self):
    pass

  def post(self):
    """ Create new user """
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str)
    parser.add_argument('display_name', type=str)
    args = parser.parse_args()

    if args.email is None or not args.email:
      abort(400, message="An e-mail address must be provided")

    if args.display_name is None or not args.display_name:
      abort(400, message="An display name must be provided")

    user = User_model()
    user.email = args.email
    user.display_name = args.display_name

    try:
      crud.add(user)
    except IntegrityError:
      abort(400, message="User %s already exists" % args.email)

    data = dict()
    data['user'] = user
    data['token'] = generate_user_token(user)
    ret_fields = {
      'token': fields.String,
      'user': fields.Nested({
        'id': fields.Integer,
        'email': fields.String,
        'display_name': fields.String
      })
    }
    return marshal(data, ret_fields), 201

  def get(self):
    """ Get a list of users """
    session = db.session
    users = session.query(User_model).all()

    data = {'users': [], 'length': 0}

    if users is not None:
      data['users'] = users
      data['length'] = len(users)

    ret_fields = {
      'length': fields.Integer,
      'users': fields.List(fields.Nested({
        'id': fields.Integer,
        'email': fields.String,
        'display_name': fields.String
      }))
    }

    return marshal(data, ret_fields), 200
