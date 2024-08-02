from flask import request, jsonify, Blueprint
from . import db
from .models import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

main = Blueprint('main', __name__)

@main.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    user = User(name=data['name'], email=data['email'], keyword=data.get('keyword'))
    db.session.add(user)
    db.session.commit()
    logger.info(f"User added: {user.name}, {user.email}, ID: {user.id}, Keyword: {user.keyword}")
    return jsonify({'message': 'User added successfully!'})

@main.route('/delete_user/<int:user_id>', methods=['DELETE'])
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
