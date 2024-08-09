from flask import request, jsonify, Blueprint, current_app
from sqlalchemy.exc import IntegrityError
from . import db
from .models import User
import logging
import jwt
import datetime
from functools import wraps
from .email import send_email

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

main = Blueprint('main', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Verifica se o token foi enviado no cabeçalho de autorização
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split()[1]  # Divide em "Bearer" e o token
            except IndexError:
                return jsonify({'message': 'Token malformado!'}), 401
        
        if not token:
            return jsonify({'message': 'Token é necessário!'}), 401

        try:
            # Decodifica o token JWT
            jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido ou expirado!'}), 401
        
        return f(*args, **kwargs)
    
    return decorated


@main.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    user = User(name=data['name'], email=data['email'])
    
    # Define a senha utilizando o método set_password
    user.set_password(data['password'])
    
    db.session.add(user)
    try:
        db.session.commit()
        send_email(user.email, 'Email cadastrado', 'Parabéns, seu email foi cadastrado com sucesso em nossa aplicação.')
        logger.info(f"User added: {user.name}, {user.email}, ID: {user.id}")
        return jsonify({'message': 'User added successfully!'})
    except IntegrityError:
        db.session.rollback()
        logger.warning(f"Email {user.email} already exists in the database.")
        return jsonify({'message': 'This email is already registered. Please use another email.'}), 400

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Busca o usuário pelo email
    user = User.query.filter_by(email=email).first()

    # Verifica se o usuário existe e se a senha está correta
    if user and user.check_password(password):
        # Gera um token JWT
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
