#app.py
from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity,JWTManager,jwt_required
import jwt
from functools import wraps
import uuid
from flask_sqlalchemy import SQLAlchemy
from model import db,User
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = b'\x06\xf5\xb5\xe6\xf7\x1c\xbd\r\xc5e\xef\xb2\xf1\xcb`\xd8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

jwt=JWTManager(app)

migrate = Migrate(app, db)
ma = Marshmallow(app)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'username', 'email', 'password', 'user_role', 'blocked', 'activity')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return({"message" : "Token is missing"})

        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
            
        except:
            return ({"message": "Invalid token"})

        return f(*args, **kwargs)
    return decorated

@app.route('/protected')
# @token_required
def protected():
    return jsonify({"message":"logged in successfully"})

@app.route('/guest')
@jwt_required()
def guest():
    return jsonify(detail="You are logged in successfully")
    
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.json.get('email',None)
        password = request.json.get('password',None)
        user = User.query.filter_by(email=email).first()
        if user:
            if user.confirm_password(password):
                token = create_access_token(identity=user.user_id)
                return jsonify(token=token)
            return jsonify(detail="password Incorrect"),401
        return jsonify(detail="User not logged in"),401

@app.route('/user', methods=['GET'])
def get_all_users():
     users = User.query.all()

     output = []

     for user in users:
        user_data = {}
        user_data['user_id'] = user.user_id
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['password'] = user.password
        user_data['user_role'] = user.user_role
        user_data['blocked'] = user.blocked
        user_data['activity'] = user.activity
        output.append(user_data)
     return jsonify({'users': output})

 
@app.route('/user/<user_id>', methods=['GET'])
def get_one_users(user_id):

    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})
    
    user_data = {}
    user_data['user_id'] = user.user_id
    user_data['username'] = user.username
    user_data['email'] = user.email
    user_data['password'] = user.password
    user_data['user_role'] = user.user_role
    user_data['blocked'] = user.blocked
    user_data['activity'] = user.activity
    return jsonify({'users': user_data})
    pass
 
@app.route('/user', methods=['POST'])
def user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='scrypt')

    new_user = User(username=data['username'],password=hashed_password, email=data['email'],user_role=data['user_role'],blocked=False,activity=False)
    db.session.add(new_user)
    db.session.commit()
    
    return ({'message':'Welcome user'})

@app.route('/user/<user_id>', methods=['PATCH'])
def promote_user(user_id):
    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})
    
    user.admin = True
    db.session.commit()

    return jsonify({'message': 'User promoted successfully'})

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User has been deleted'})
    

if __name__ == '__main__':
    app.run(debug=True)
