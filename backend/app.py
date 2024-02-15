from flask import request, Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80),unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)

    def json(self):
        return {'id':self.id, 'name':self.name, 'email':self.email}
    
db.create_all()

# test
@app.route('/test',methods = ['GET'])
def test():
    return jsonify({'message': 'The server is running'})

# create user
@app.route('/api/flask/users', methods = ['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(name = data['name'], email = data['email'])
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'id': new_user.id,
            'name':new_user.name,
            'email':new_user.email
        }), 201
    except Exception as e:
        return make_response(({'message': 'error createing user ', 'error':str(e)}), 500)
    
# get all user
@app.route('/api/flask/users', methods = ['GET'])
def get_users():
    try:
        users = User.query.all()
        user_data = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]

        return jsonify(user_data), 200

    except Exception as e:
        return make_response(({'message': 'error getting users', 'error': str(e)}), 500)
    
# get a user with id
@app.route("/api/flask/users/<int:user_id>", methods=['GET'])
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return make_response(jsonify({'user':user.json()}), 200)
        return make_response(jsonify({'message':'user not found'}), 404)
    except Exception as e:
        return make_response(({'message': 'error getting user', 'error': str(e)}), 500)

# update user
@app.route('/api/flask/user/<int:user_id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.name = data['name']
            user.email = data['email']
            db.session.commit()
            return make_response(jsonify({'message': 'user updated'}), 200)
        return make_response(jsonify({'message':'user not found'}), 404)
    
    except Exception as e:
        return make_response(({'message': 'error updating user', 'error': str(e)}), 500)

# delete user 
@app.route('/api/flask/user/<int:user_id>', methods=['DELETE'])
def delete_user(id):
    
    try:
        user = User.query.filter_by(id=id).first()

        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'message': 'user deleted sucefully'}), 200)
        return make_response(jsonify({'message':'user not found'}), 404)
    except Exception as e:
        return make_response(({'message': 'error deleting user', 'error':str(e)}),500)
