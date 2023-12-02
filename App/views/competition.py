from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required
from datetime import datetime, date


from App.controllers import *


competition_views = Blueprint('competition_views', __name__, template_folder='../templates')


'''
Page Routes
'''
@competition_views.route('/competition', methods=['GET'])
@admin_required
def competition_form_page():
    return render_template('competition_form.html')

@competition_views.route('/competitions', methods=['GET'])
def competition_page():
    competitions = get_all_competitions()
    return render_template('competitions.html', competitions=competitions)

@competition_views.route('/competition/details', methods=['GET'])
def competition_details_page():
    competition_id = request.args.get('competition_id')
    competition = get_competition_by_id(competition_id)
    page = request.args.get('page', 1, type=int)
    results = get_results_by_competition_id(competition_id, page=page)
    return render_template('competition_details.html', competition=competition, results=results, page=page)


'''
Action Routes
'''
@competition_views.route('/competition', methods=['POST'])
@admin_required
def add_competition_action():
    competition_name = request.form.get('competitionName')
    location = request.form.get('location')
    platform = request.form.get('platform')    
    date = request.form.get('date')
    competition_date = datetime.strptime(date, '%Y-%m-%d')   
    response = create_competition(name=competition_name, location=location, platform=platform, date=competition_date)
    if response:
        flash('Competition created successfully!')
        return redirect(url_for('competition_views.competition_form_page'))
    flash('Error creating competition')
    return redirect(url_for('competition_views.competition_form_page'))



'''
API Routes
'''

@competition_views.route('/api/competitions', methods=['GET'])
def api_get_all_competitons():
    competitions = get_all_competitions_json()
    if competitions:
        return (jsonify(competitions),200) 
    return jsonify({'message': 'No Competitions found'}), 405

@competition_views.route('/api/competition', methods=['POST'])
@admin_required
def add_new_competition_views():
    data = request.json
    name= data.get('name')
    location = data.get('location')
    platform = data.get('platform')

    if None in (name, location, platform, data['date']):
        return jsonify({'error': 'Missing data in the request'}), 400
  
    response = create_competition(name=name, location=location, platform=platform, date=datetime.strptime(data['date'], "%Y-%m-%d"))
    
    if response:
        return (jsonify({'message': f"Competition created"}), 201)
    return (jsonify({'error': f"Error creating competition"}),500)


@competition_views.route('/api/competition/details/<int:id>', methods=['GET'])
def get_competition_views(id):
    competition_details = get_competition_details(id)
    if not competition:
        return jsonify({'error': 'competition not found'}), 404          
    return (jsonify(competition_details),200)

@competition_views.route('/api/competition/details/<int:id>', methods=['GET'])
def get_competition_views(id):
    competition = get_competition_details(id)
    if not competition:
        return jsonify({'error': 'competition not found'}), 404     
    return (jsonify(competition),200)




