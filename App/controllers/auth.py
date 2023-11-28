from flask_login import login_user, login_manager, logout_user, LoginManager, current_user
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from functools import wraps
from flask import jsonify

from App.models import User, Admin, Competitor

def jwt_authenticate(username, password):
    user = Admin.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return create_access_token(identity=username)

    user = Competitor.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return create_access_token(identity=username)
    return None

def login(username, password):
    user = Admin.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user

    user = Competitor.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None

def setup_flask_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        
        user = Admin.query.get(user_id)
        if user:
            return user
        
        return Competitor.query.get(user_id)
    
    return login_manager

def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        user = Admin.query.filter_by(username=identity).one_or_none()
        if user:
            return user.id
        
        user = Competitor.query.filter_by(username=identity).one_or_none()
        if user:
            return user.id
        return None

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.get(identity)

    return jwt

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Admin):
            return jsonify({"error" : "Permission Denied. This action is restricted to admin only" }), 401
        return func(*args, **kwargs)
    return wrapper

def competitor_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Competitor):
            return jsonify({"error" : "Permission Denied. This action is restricted to admin only" }), 401
        return func(*args, **kwargs)
    return wrapper