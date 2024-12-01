import email
import bcrypt
from flask import jsonify
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError

from ..models import User
from ..schemasDTO.in_user_schemas import LoginSchema, RegisterSchema
from ..database import db


def login(request_body):
    schema = LoginSchema()
    try:
        data = schema.load(request_body)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({'message': 'Invalid email or password'}), 401

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={'email': user.email, 'role': user.role}
    )
    return jsonify({'token': access_token}), 200

def register(request_body):
    schema = RegisterSchema()
    try:
        data = schema.load(request_body)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    user = User.query.filter_by(email=data['email']).first()
    if user:
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(
        email=data['email'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        role=data['role'],
        password=bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201