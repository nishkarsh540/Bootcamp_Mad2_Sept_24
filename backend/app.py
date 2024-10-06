from flask import Flask,jsonify,make_response
from flask_restful import Api,Resource,reqparse
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash,check_password_hash
from model import db,User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
app.config['JWT_SECRET_KEY'] = 'grocery'


db.init_app(app)
CORS(app,origins='*')
jwt = JWTManager(app)
api = Api(app)

class SignupResource(Resource):
    def post(self):
        parser= reqparse.RequestParser()
        parser.add_argument('username',type=str,required=True,help='Username is required')
        parser.add_argument('password',type=str,required=True)
        parser.add_argument('role',type=str,default='user')
        args=parser.parse_args()

        if User.query.filter_by(username=args['username']).first():
            return {'message':'username already exists'},400

        if args['role'] == 'user':

            hashed_password = generate_password_hash(args['password'])

            new_user = User(username=args['username'],password=hashed_password,role=args['role'],approved=True)
        else: 
            hashed_password = generate_password_hash(args['password'])

            new_user = User(username=args['username'],password=hashed_password,role=args['role'])

        db.session.add(new_user)
        db.session.commit()

        return {'message':'user created succesfully'},200
    

class LoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username',type=str,required=True)
        parser.add_argument('password',type=str,required=True)
        args=parser.parse_args()

        user = User.query.filter_by(username=args['username']).first()
        if user and check_password_hash(user.password,args['password']):
            access_token = create_access_token(identity=user.role)
            user_info = {
                "id":user.id,
                "username":user.username,
                "role":user.role
            }

            return {'access_token':access_token,"user":user_info}, 200
        else:
            return {'message':'Invalid Username or password'},401



class UserInfo(Resource):
    def get(self):
        users = User.query.all()
        user_info = [{
            "id":user.id,
            "username":user.username
        } for user in users]

        return user_info

api.add_resource(SignupResource,'/api/signup')
api.add_resource(LoginResource,'/api/login')
api.add_resource(UserInfo,'/userinfo')
if __name__ == "__main__":
    app.run(debug=True)