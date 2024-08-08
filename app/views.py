from flask import request, jsonify, Blueprint
from sqlalchemy.exc import IntegrityError
from . import db
from .models import User
import logging
from .email import send_email

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

main = Blueprint('main', __name__)

@main.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    user = User(name=data['name'], email=data['email'], keyword=data.get('keyword'))
    db.session.add(user)
    try:
        db.session.commit()
        send_email(user.email, 'Email cadastrado', 'Parabens seu email foi cadastrado com sucesso em nossa aplicação.')
        logger.info(f"User added: {user.name}, {user.email}, ID: {user.id}, Keyword: {user.keyword}")
        return jsonify({'message': 'User added successfully!'})
    except IntegrityError:
        db.session.rollback()
        logger.warning(f"Email {user.email} already exists in the database.")
        return jsonify({'message': 'This email is already registered. Please use another email.'}), 400

@main.route('/delete_user/<string:user_id>', methods=['DELETE'])  # Alterado de <int> para <string>
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
            'keyword': user.keyword
        }
        result.append(user_data)
    logger.info(f"Users in database: {result}")
    return jsonify(result)
