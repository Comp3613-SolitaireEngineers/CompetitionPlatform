from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required# current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user
from App.models import db
from App.controllers import *


auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

'''
Page Routes
'''

@auth_views.route('/signup', methods=['GET'])
def signup_page():
  return render_template('signup.html')



@auth_views.route('/login', methods = ['GET'])
def login_page():  
  referrer=request.referrer  
  return render_template('login.html', referrer=referrer)


'''
Action Routes
'''

@auth_views.route('/login', methods = ['POST'])
def login_action():
  
  data = request.form # get login credentials from frontend form

  # get login credentials from json eg postman api test
  if not data:
    data = request.json

  # print(list(data.keys()))
  # print(list(data.values()))

  if 'email' not in data or 'password' not in data:
    flash('Error: Missing email or password.')
    return jsonify(error='Missing email or password.'), 400

  email = data.get('email')
  password = data.get('password')

  competitor = Competitor.query.filter_by(email=email).first()
  if competitor and competitor.check_password(password):
    logout_user()
    login_user(competitor)
    # token = jwt_authenticate(data['email'], data['password'])
    # if not token:
    #   return jsonify(error='bad email or password given'), 401

    # print(current_user.username)
    # return jsonify(message="competitor logged in"), 200
    return redirect(data.get('referrer', '/')), 200  # redirects to '/' if 'referrer' is missing

  admin = Admin.query.filter_by(email=email).first()
  if admin and admin.check_password(password):
    logout_user()
    login_user(admin)
    # token = jwt_authenticate(data['email'], data['password'])
    # if not token:
    #     return jsonify(message='bad email or password given'), 401

    # print(current_user.username)
    return redirect('/competition'), 200
  
  return jsonify(error="user does not exist"), 404

@auth_views.route('/signup', methods=['POST'])
def signup_action():
  
  try:
    data = request.form # get login credentials from frontend form

    # get login credentials from json eg postman api test
    if not data:
      data = request.json

    # print(list(data.keys()))
    # print(list(data.values()))

    competitor = create_competitor(uwi_id=data['uwi_id'], firstname=data['firstname'], lastname=data['lastname'], username=data['username'], password = data['password'], email=data['email'])
    login_user(competitor)

    if competitor:
      flash('Account Created!')  
      # return jsonify(message='Account created'), 201
      return redirect("/leaderboard"), 201

  except Exception as e:      
    print("Error in signup: ", e)
    flash("Username, Email, or UWI ID has an existing account associated with it")  # error message
    return jsonify(error='Username, Email, or UWI ID has an existing account associated with it'), 401


@auth_views.route('/identify', methods=['GET'])
def identify_page():
    if current_user.is_authenticated:
      return jsonify({'message': f"{current_user.get_json()}"}) 
    return jsonify({'message': "Not Logged In"})

# @auth_views.route('/password-change', methods=['POST'])
# def password_change_action():
#     data = request.form
#     if current_user.update_admin_password(data['newPassword']):
#       current_user.is_password_changed = True
#       db.session.commit()
#       flash("Changed Succesfully")
#       return redirect('/projects')
    
#     flash("Try Again!")
#     return redirect(request.referrer)
  
@auth_views.route('/logout', methods=['GET'])
def logout_action():
    logout()
    flash('Logged Out!')
    return redirect('/leaderboard')

'''
API Routes
'''

# @auth_views.route('/api/users', methods=['GET'])
# def get_users_action():
#     users = get_all_users_json()
#     return jsonify(users)

# @auth_views.route('/api/users', methods=['POST'])
# def create_user_endpoint():
#     data = request.json
#     response = create_user(data['username'], data['password'])
#     if response:
#         return jsonify({'message': f"user created"}), 201
#     return jsonify(error='error creating user'), 500

# @auth_views.route('/api/login', methods=['POST'])
# def user_login_api():
#   data = request.json
#   token = jwt_authenticate(data['username'], data['password'])
#   if not token:
#     return jsonify(error='bad username or password given'), 401
#   return jsonify(access_token=token)

# @auth_views.route('/api/identify', methods=['GET'])
# @jwt_required()
# def identify_user_action():
#     return jsonify({'message': f"username: {jwt_current_user.username}, id : {jwt_current_user.id}"})


