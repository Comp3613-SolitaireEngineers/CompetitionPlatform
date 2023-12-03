from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required
from App.controllers import *
from werkzeug.utils import secure_filename
from os import remove


results_views = Blueprint('results_views', __name__, template_folder='../templates')


'''
Page Routes
'''
@results_views.route('/competition/results', methods=['GET'])
@admin_required
def competition_results_page():
    competitions = get_all_competitions()
    competition_id = request.args.get('competition_id')
   
    competition = get_competition_by_id(competition_id)
    page = request.args.get('page', 1, type=int)
    results = get_results_by_competition_id(competition_id, page=page)
    return render_template('competition_results.html', competitions=competitions, competition=competition, results=results, selected_competition_id=competition_id, page=page)



'''
Action Routes
'''

@results_views.route('/results', methods=['POST'])
@admin_required
def add_results_action():
    
    

    competition_id = request.form.get('competition_id')
    if competition_id is None:
        flash('Please select a competition')
        return redirect(request.referrer)
    
    competition = get_competition_by_id(competition_id)
    if competition is None:
        flash('Competition not found')
        return redirect(request.referrer)
    
    competitions = get_all_competitions()
    


    try:
        file = request.files['result_file']
        results_file = file
        new_name = secure_filename(results_file.filename)
        results_file.save(f"App/static/{new_name}")
        results_file_path = f"App/static/{new_name}"                
        response = add_results(competition_id, results_file_path)

        page = request.args.get('page', 1, type=int)
        results = get_results_by_competition_id(competition.id, page=page)
        if response is None:
            flash('Results already added for this competition')
            render_template('competition_results.html', competitions=competitions, competition=competition, results=results, selected_competition_id=competition_id, page=page)

        remove(f"App/static/{new_name}")
        flash("Results added successfully!")        
        return render_template('competition_results.html', competitions=competitions, competition=competition, results=results, selected_competition_id=competition_id, page=page)
    except Exception as e:
        # Handle exceptions (e.g., file not found, incorrect format)
        print(e)
        flash('Error uploading file. Please try again.')
        return redirect(request.referrer)#return render_template('competition_results.html', competitions=competitions, competition=competition, results=results, selected_competition_id=competition_id, page=page)


@results_views.route('/competition/results', methods=['POST'])
@admin_required
def competition_results_action():
    competition_id = request.form.get('competition')

    if(competition_id is None):
        return redirect(request.referrer)
    
    page = request.args.get('page', 1, type=int)    
    competition = get_competition_by_id(competition_id)
    results = get_results_by_competition_id(competition_id, page=page)
    competitions = get_all_competitions()         
    return render_template('competition_results.html', competitions=competitions,competition=competition, selected_competition_id=competition_id, results=results, page=page)



'''
API Routes
'''

@results_views.route('/api/results', methods=['POST'])
def api_create_results():
    data = request.json
    competition_id = data['competition_id']
    competitor_id = data['competitor_id']
    points = data['points']
    rank = data['rank']

    if None in (competition_id, competitor_id, points, rank):
        return jsonify({'error': 'Missing data in the request'}), 400

    result = create_result(competition_id, competitor_id, points, rank)
    if result:
        return jsonify(result.get_json()), 200
    else:
        return jsonify({'message': 'Result not created'}), 405



@results_views.route('/api/results', methods=['GET'])
def api_get_results():
    results = get_all_results_json()
    if results:
        return (jsonify(results),200)
    return jsonify({'message': 'No Results found'}), 405


@results_views.route('/api/results/<competition_id>', methods=['GET'])
def api_get_competition_results(competition_id):
    results = get_results_by_competition_id(competition_id)
    if results:
        return jsonify(results), 200
    else:
        return jsonify({'message': 'Competition Results not found'}), 405

