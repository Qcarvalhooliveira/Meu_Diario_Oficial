from flask import request, jsonify, Blueprint, current_app
from sqlalchemy.exc import IntegrityError
from . import db
from .models import User
import logging
import jwt
import datetime
from functools import wraps
from .email import send_email, generate_welcome_email

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a blueprint for the main routes
main = Blueprint('main', __name__)

def token_required(f):
    """
    Decorator that checks if a valid JWT token is provided in the request headers.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check if the token is provided in the 'Authorization' header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split()[1]  # Split to get the token part
            except IndexError:
                return jsonify({'message': 'Token malformado!'}), 401
        
        if not token:
            return jsonify({'message': 'Token é necessário!'}), 401

        try:
            # Decode the JWT token
            jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido ou expirado!'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

@main.route('/add_user', methods=['POST'])
def add_user():
    """
    Route to add a new user to the database.
    """
    data = request.get_json()
    user = User(name=data['name'], email=data['email'])
    
    # Hash the user's password using set_password method
    user.set_password(data['password'])
    
    db.session.add(user)
    try:
        db.session.commit()

        # Generate the welcome email body
        logo_url = "http://www.dom.salvador.ba.gov.br/images/stories/logo_diario.png"
        email_body = generate_welcome_email(user.name, logo_url)

        # Send the welcome email
        send_email(user.email, 'Email cadastrado com sucesso!', email_body)

        logger.info(f"User added: {user.name}, {user.email}, ID: {user.id}")
        return jsonify({'message': 'User added successfully!'})
    except IntegrityError:
        db.session.rollback()
        logger.warning(f"Email {user.email} already exists in the database.")
        return jsonify({'message': 'This email is already registered. Please use another email.'}), 400

@main.route('/login', methods=['POST'])
def login():
    """
    Route to log in a user.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Fetch the user by email
    user = User.query.filter_by(email=email).first()

    # Verify the user's password
    if user and user.check_password(password):
        # Generate a JWT token
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')

        logger.info(f"User logged in: {user.name}, {user.email}, ID: {user.id}")
        return jsonify({'token': token})
    else:
        logger.warning(f"Failed login attempt for email: {email}")
        return jsonify({'message': 'Email ou senha incorretos!'}), 401

@main.route('/delete_user/<string:user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    """
    Route to delete a user by their ID.
    """
    user = db.session.get(User, user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        logger.info(f"User deleted: {user.name}, {user.email}, ID: {user.id}")
        return jsonify({'message': 'User deleted successfully!'})
    else:
        logger.warning(f"User not found: ID {user_id}")
        return jsonify({'message': 'User not found!'}), 404

@main.route('/users', methods=['GET'])
def get_users():
    """
    Route to retrieve all fusers in the database.
    THIS ROUTE IS FOR DEVELLOPMENT ONLY to allow the dev to see all users on database. for security in PROD we would exclude this route and leave only the one that get users by id
    """
    users = User.query.all()
    result = []
    for user in users:
        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
        }
        result.append(user_data)
    logger.info(f"Users in database: {result}")
    return jsonify(result)

@main.route('/user', methods=['GET'])
@token_required
def get_user():
    """
    Route to retrieve the authenticated user's information.
    The user ID is extracted from the JWT token.
    """
    # Extract the token from the headers
    token = None
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        try:
            token = auth_header.split()[1]  # Extract the token part
        except IndexError:
            return jsonify({'message': 'Token malformado!'}), 401

    if not token:
        return jsonify({'message': 'Token é necessário!'}), 401

    try:
        # Decode the JWT token to extract the user_id
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = data['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expirado!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Token inválido ou expirado!'}), 401

    # Query the user by their ID
    user = User.query.get(user_id)
    
    if not user:
        logger.warning(f"User with ID {user_id} not found.")
        return jsonify({'message': 'User not found'}), 404
    
    # Prepare the user data to be returned
    user_data = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
    }

    logger.info(f"User retrieved: {user_data}")
    return jsonify(user_data), 200
