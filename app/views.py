from flask import request, jsonify, Blueprint
from . import db
from .models import User, Subscription

main = Blueprint('main', __name__)

@main.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    user = User(name=data['name'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User added successfully!'})

@main.route('/add_subscription', methods=['POST'])
def add_subscription():
    data = request.get_json()
    subscription = Subscription(user_id=data['user_id'], keyword=data['keyword'])
    db.session.add(subscription)
    db.session.commit()
    return jsonify({'message': 'Subscription added successfully!'})
