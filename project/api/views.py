from flask import Blueprint, jsonify, request
from project.api.models import User
from project import db

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

@users_blueprint.route('/users', methods=['POST'])
def add_user():
    post_data = request.get_json()
    if not post_data:
        response_object = {'status': 'fail', 'message':'Invalid payload'}
        return jsonify(response_object), 400
    username = post_data.get('username')
    email = post_data.get('email')
    if not username or not email:
        response_object = {'status':'fail', 'message':'Invalid payload keys'}
        return jsonify(response_object), 400
    db.session.add(User(username=username, email=email))
    db.session.commit()
    response_object = {
        'status':'success',
        'message':f'{email} was added!'
    }
    return jsonify(response_object), 201