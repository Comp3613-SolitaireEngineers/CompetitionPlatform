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
    competition = get_competition_by_id(id)
    if not competition:
        return jsonify({'error': 'competition not found'}), 404 
    
    competition_details = {
        "name": competition.name,
        "location": competition.location,
        "platform": competition.platform,
        "date": competition.date,        
    }
    return (jsonify(competition_details),200)


# @comp_views.route('/api/competitions/<int:id>', methods=['GET'])
# def get_competition_views(id):
#     competition = get_competition_by_id(id)
#     if not competition:
#         return jsonify({'error': 'competition not found'}), 404 
#     return (jsonify(competition.toDict()),200)

# @comp_views.route('/api/competition/<string:id>/competitors', methods=['GET'])
# def get_competition_competitors_views(id):
#     competition = get_competition_by_id(id)
    
#     if not competition:
#         return jsonify({'message': 'competition does not exist'}),404 
        
#     competitors = get_competition_competitors(id)
    
#     if competitors:
#         return jsonify(competitors), 200
    
#     return jsonify({'message': 'no competitors found'}), 404



# @comp_views.route('/competitions/results', methods=['POST'])
# def add_comp_results():
#     data = request.json
#     response = add_user_to_comp(data['user_id'],data['comp_id'], data['rank'])
#     if response:
#         return (jsonify({'message': f"results added successfully"}),201)
#     return (jsonify({'error': f"error adding results"}),500)




