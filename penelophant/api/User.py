""" User API representation object """

from sqlalchemy.exc import IntegrityError
from flask_restful import Resource, abort, reqparse
from penelophant.models.User import User as User_model
from penelophant.database import db
from penelophant import crud

class User(Resource):
  """ Specific user API """

  def __init__(self):
    pass

  def get(self, user_id):
    """ Retrieve user """
    user = self.get_user_by_id_or_abort(user_id)
    return user.to_api(), 200

  def delete(self, user_id):
    """ Delete user """
    user = self.get_user_by_id_or_abort(user_id)
    crud.delete(user)
    return '', 204

  def put(self, user_id):
    """ Update a user """
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str)
    args = parser.parse_args()

    user = self.get_user_by_id_or_abort(user_id)
    user.email = args.email
    crud.save()

    return user.to_api(), 200

  def get_user_by_id_or_abort(self, user_id):
    """ Attempt to get user by id, or abort if it goes south """
    user_id = int(user_id)
    session = db.session
    user = session.query(User_model).filter(User_model.id == user_id).first()
    if not user:
      abort(404, message="User {} doesn't exist".format(user_id))
    return user

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
    return user.to_api(), 201

  def get(self):
    """ Get a list of users """
    session = db.session
    users = session.query(User_model).all()

    data = dict()
    data['users'] = [user.to_api() for user in users]
    data['count'] = len(users)

    return data
