from flask import Flask, request, jsonify
from models import db, User
import bcrypt
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# Connect to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    
    # Validate required fields
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400
    
    # Validate password strength
    if len(data['password']) < 8:
        return jsonify({'error': 'Password must be at least 8 characters long'}), 400
    
    # Hash the password with bcrypt
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    
    new_user = User(username=data['username'], password=hashed_password.decode('utf-8'), active=data.get('active', True))
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Username already exists'}), 400
    
    return jsonify({'message': 'User created successfully', 'data': {'id': new_user.id, 'username': new_user.username}}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'active': user.active} for user in users])

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id=None):
    if not id:
        return jsonify({'error': 'User ID is required'}), 400
    
    user = User.query.get(id)
    if user is None:
        return jsonify({'error': f'User with ID {id} does not exist'}), 404
    
    return jsonify({'id': user.id, 'username': user.username, 'active': user.active})



@app.route('/users/update/<int:id>', methods=['POST'])
def update_user(id):
    data = request.json
    user = User.query.get(id)
    
    if user is None:
        return jsonify({'error': f'User with ID {id} does not exist'}), 404
    
    # Validate required fields
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400
    
    # Validate password strength
    if len(data['password']) < 8:
        return jsonify({'error': 'Password must be at least 8 characters long'}), 400
    
    # Check if the username is taken by another user
    existing_user = User.query.filter(User.username == data['username'], User.id != id).first()
    if existing_user:
        return jsonify({'error': f'Username {data["username"]} is already taken by another user'}), 400
    
    # Update the user's details
    user.username = data['username']
    user.password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user.active = data.get('active', user.active)
    
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while updating the user'}), 500
    
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'error': f'User with ID {id} does not exist'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)