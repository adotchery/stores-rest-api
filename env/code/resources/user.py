from db import db
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    #add parser
    parser = reqparse.RequestParser()
    parser.add_argument("username",
        type=str,
        required=True,
        help="this field cannot be blank"
    )
    parser.add_argument("password",
        type=str,
        required=True,
        help="this field cannot be blank"
    )

    def post(self):
        #add data for the username and password
        data = UserRegister.parser.parse_args()
        #checking for dulicate username
        if UserModel.find_by_username(data['username']):
            return {"message":"This username already exist!"},400

        #connect the DB
        user = UserModel(**data)
        user.save_to_db()

        return {"message":"User created successfully"}, 201
