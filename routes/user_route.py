from models import db
from flask import Blueprint
from models.user import User
from utils.utils import get_response
from utils.decorators import login_required
from flask_restful import Api, Resource, reqparse

user_create_parse = reqparse.RequestParser()
user_create_parse.add_argument("full_name", type=str, required=True, help="Full Name cannot be blank")
user_create_parse.add_argument("phone_number", type=str, required=True, help="Phone Number cannot be blank")
user_create_parse.add_argument("username", type=str, required=True, help="Username cannot be blank")
user_create_parse.add_argument("password", type=str, required=True, help="Password cannot be blank")

user_update_parse = reqparse.RequestParser()
user_update_parse.add_argument("full_name", type=str)
user_update_parse.add_argument("phone_number", type=str)
user_update_parse.add_argument("username", type=str)
user_update_parse.add_argument("password", type=str)

user_bp = Blueprint("user", __name__, url_prefix="/api/user")
api = Api(user_bp)

class UserResource(Resource):
    decorators = [login_required()]
    
    def get(self, user_id):
        """User Get API
        Path - /api/user/<user_id>
        Method - GET
        ---
        consumes: application/json
        parameters:
            - in: header
              name: Authorization
              type: string
              required: true
              description: Bearer token for authentication

            - name: user_id
              in: path
              type: integer
              required: true
              description: Enter User ID
        responses:
            200:
                description: Return a User
            404:
                description: User not found
        """
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return get_response("User not found", None, 404), 404
        
        return get_response("User successfully found", User.to_dict(user), 200), 200

    def delete(self, user_id):
        """User Delete API
        Path - /api/user/<user_id>
        Method - DELETE
        ---
        consumes: application/json
        parameters:
            - in: header
              name: Authorization
              type: string
              required: true
              description: Bearer token for authentication
              
            - name: user_id
              in: path
              type: integer
              required: true
              description: Enter User ID
        responses:
            200:
                description: Delete a User
            404:
                description: User not found
        """
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return get_response("User not found", None, 404), 404
        
        db.session.delete(user)
        db.session.commit()
        return get_response("Successfully deleted user", None, 200), 200
    
    def patch(self, user_id):
        """User Update API
        Path - /api/user/<user_id>
        Method - PATCH
        ---
        consumes: application/json
        parameters:
            - in: header
              name: Authorization
              type: string
              required: true
              description: Bearer token for authentication

            - name: user_id
              in: path
              type: integer
              required: true
              description: Enter User ID

            - name: body
              in: body
              required: true
              schema:
                type: object
                properties:
                    full_name: 
                        type: string
                    phone_number:
                        type: string
                    username:
                        type: string
                    password:
                        type: string
        responses:
            200:
                description: Successfully updated user
            404:
                description: User not found
        """
        found_user = User.query.filter_by(id=user_id).first()
        if not found_user:
            return get_response("User not found", None, 404), 404
        
        data = user_update_parse.parse_args()
        full_name = data.get('full_name', None)
        phone_number = data.get('phone_number', None)
        username = data.get('username', None)
        password = data.get('password', None)

        if full_name is not None:
            found_user.full_name = full_name
        if phone_number is not None:
            found_user.phone_number = phone_number
        if username is not None:
            found_user.username = username
        if password is not None:
            found_user.password = password
       
        db.session.commit()
        return get_response("Successfully updated user", None, 200), 200

class UserListCreateResource(Resource):
    decorators = [login_required()]

    def get(self):
        """User List API
        Path - /api/user
        Method - GET
        ---
        consumes: application/json
        parameters:
            - in: header
              name: Authorization
              type: string
              required: true
              description: Bearer token for authentication

        responses:
            200:
                description: Return User List
        """
        user_list = User.query.filter_by().order_by(User.created_at.desc()).all()
        result_user_list = [User.to_dict(user) for user in user_list]
        return get_response("User List", result_user_list, 200), 200

    def post(self):
        """User Create API
        Path - /api/user
        Method - POST
        ---
        consumes: application/json
        parameters:
            - in: header
              name: Authorization
              type: string
              required: true
              description: Bearer token for authentication

            - name: body
              in: body
              required: true
              schema:
                type: object
                properties:
                    full_name: 
                        type: string
                    phone_number:
                        type: string
                    username:
                        type: string
                    password:
                        type: string
                required: [full_name, phone_number, username, password]
        responses:
            200:
                description: Return New User ID
            400:
                description: (Full Name, Phone Number, Username or Password is Blank) or (Phone Number already taken or Username already taken)
        """
        data = user_create_parse.parse_args()
        full_name = data['full_name']
        phone_number = data['phone_number']
        username = data['username']
        password = data['password']

        user = User.query.filter_by(phone_number=phone_number).first()
        if user:
            return get_response("Phone Number already exists", None, 400), 400
        
        user = User.query.filter_by(username=username).first()
        if user:
            return get_response("Username already exists", None, 400), 400
        
        new_user = User(full_name, phone_number, username, password)
        db.session.add(new_user)
        db.session.commit()
        return get_response("Successfully created user", new_user.id, 200), 200

api.add_resource(UserResource, "/<user_id>")
api.add_resource(UserListCreateResource, "/")
