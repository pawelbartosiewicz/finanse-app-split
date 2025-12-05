from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from app import db
from datetime import datetime
from werkzeug.security import check_password_hash
from app.models import User, generate_password_hash
from app import login_manager




auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user, remember=True)
            
        return jsonify({
            "message": "Zalogowano pomyślnie!",
            "username": user.username,
            "user_id": user.id,
            "hashed_password" : user.password_hash,
            "email": user.email
        }), 200
    else:
        return jsonify({
            "error": "Błędny email lub hasło"
        }), 401


@auth_bp.route('/api/logout', methods=['POST'])
@login_required
def logout():
    
    if not current_user.is_authenticated:
        return jsonify({
            "message" : "You are not logged in!"
            }),401

    if current_user.is_authenticated:
        logout_user()
        return jsonify({
            "message" : "You have been logged out!"
        }), 200



# check if user is authenticated
@auth_bp.route('/api/isLoggedIn', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return jsonify({
            "message" : f"You are logged in, hello {current_user.username}!",
        })
    else:
        return jsonify({
            "message" : "You are not logged in, hello!",

        })
    





@auth_bp.route('/api/register', methods=['POST'])
def register():

    if current_user.is_authenticated:
        return jsonify({
            "message": "You are already logged in!"
        }), 400
    else:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not User.query.filter_by(username=username).first():
            hashed_password = generate_password_hash(password)

            userToRegister = User(
                username=username, 
                password_hash=generate_password_hash(password),  
                created_at=datetime.now(),
                email=email
            )

    # 4. Dodaj do bazy
    try:
        db.session.add(userToRegister)
        db.session.commit()
        return jsonify({
            "message": "User registered successfully!",
            "username": userToRegister.username,
            "email": userToRegister.email
        }), 201
    except Exception as e:
        db.session.rollback()
        print(f"Wystąpił błąd bazy danych: {e}")
