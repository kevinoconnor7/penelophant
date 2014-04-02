""" User API representation object """

from flask import g
from sqlalchemy.exc import IntegrityError
from flask_restful import Resource, abort, reqparse
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
    return user.to_api(), 200

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
    args = parser.parse_args()

    user = get_user_by_id_or_abort(user_id)

    if user != g.user:
      abort(403, message="Not authorized to update user")

    user.email = args.email
    crud.save()

    return user.to_api(), 200

class UserList(Resource):
  """ User index API """

  def __init__(self):
    pass

  def post(self):
    """ Create new user """
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str)
    args = parser.parse_args()

    user = User_model()
    user.email = args.email

    try:
      crud.add(user)
    except IntegrityError:
      abort(400, message="User %s already exists" % args.email)

    data = dict()
    data['user'] = user.to_api()
    data['token'] = generate_user_token(user).decode('ascii')
    return user.to_api(), 201

  def get(self):
    """ Get a list of users """
    session = db.session
    users = session.query(User_model).all()

    data = dict()
    data['users'] = [user.to_api() for user in users]
    data['count'] = len(users)

    return data
