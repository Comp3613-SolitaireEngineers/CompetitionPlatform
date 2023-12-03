from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required
from App.controllers import *


competitor_views = Blueprint('competitor_views', __name__, template_folder='../templates')



'''
Page Routes
'''
@competitor_views.route('/competitor/profile', methods=['GET'])
@competitor_required
def competitor_profile_page():
    flash('Welcome to your profile')
    notifications = get_competitor_notifications(current_user.id)
    return render_template('competitor_profile.html', notifications_info=notifications)

@competitor_views.route('/seen/<notification_id>', methods=['POST'])
@competitor_required
def seen_action(notification_id):
    reponse = seen_notification(notification_id)
    if reponse:
        return jsonify({'message': 'Notification seen'})
    return jsonify({'message': 'Notification not seen'}), 400






'''
Action Routes
'''



'''
API Routes
'''

@competitor_views.route('/api/competitors', methods=['GET'])
def api_get_competitors():
    competitors = get_all_competitors_json()
    if competitors:
        return (jsonify(competitors),200)
    return jsonify({'message': 'No Competitors found'}), 404


@competitor_views.route('/api/competitor', methods=['POST'])
def api_add_new_competitor():    
    data = request.json    
    uwi_id = data.get('uwi_id')
    email = data.get('email')
    username = data.get('username')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    password = data.get('password')

    if None in (uwi_id, first_name, last_name, password, email, username):
        return jsonify({'error': 'Missing data in the request'}), 400

    competitor = create_competitor( uwi_id=uwi_id, username=username, firstname=first_name, lastname=last_name, password=password, email=email)
   
    
    if competitor:
        return jsonify({'message': 'Competitor created successfully'}), 201
    else:
        return jsonify({'error': 'Competitor not created'}), 400
    
@competitor_views.route('/api/competitor/profile/<id>', methods=['GET'])
def api_get_competitor_by_id(id):
    competitor_profile = get_competitor_profile(id)   
    if competitor_profile:                     
        return jsonify(competitor_profile), 200
    return jsonify({'message': 'Competitor not found'}), 404