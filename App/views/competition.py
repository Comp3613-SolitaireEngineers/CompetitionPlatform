from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required
from App.controllers import get_all_competitions_json, create_competition, get_competition_by_id, get_competition_competitors

from.index import index_views

from App.controllers import (
    
     jwt_authenticate, 
    jwt_required
    
)


comp_views = Blueprint('comp_views', __name__, template_folder='../templates')

# @comp_views.route('/api/competitions', methods=['GET'])
# def get_competitons_views():
#     competitions = get_all_competitions_json()
#     return (jsonify(competitions),200) 

# @comp_views.route('/api/competition', methods=['POST'])
# def add_new_competition_views():
#     data = request.json
#     response = create_competition(data['name'], data['location'])
#     if response:
#         return (jsonify({'message': f"competition created"}), 201)
#     return (jsonify({'error': f"error creating competition"}),500)

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




