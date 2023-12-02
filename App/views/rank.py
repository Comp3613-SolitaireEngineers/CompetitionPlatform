from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required
from App.controllers import *

rank_views = Blueprint('rank_views', __name__, template_folder='../templates')

@rank_views.route('/api/ranks', methods=['GET'])
def api_get_ranks():
    ranks = get_rankings()
    if ranks:
        return (jsonify(ranks),200)
    return jsonify({'message': 'No Ranks found'}), 405
    
@rank_views.route('/api/rank/<competitor_id>', methods=['GET'])
def api_get_competitor_rank(competitor_id):
    rank = get_rank_by_competitor_id(competitor_id)
    if rank:
        return jsonify(rank.get_json()), 200
    else:
        return jsonify({'message': 'Competitor Rank not found'}), 405
    
@rank_views.route('/api/rank/ranking', methods=['PUT'])
@admin_required
def api_update_rank():
    data = request.json
    rank = update_rank(competitor_id=data["competitor_id"], ranking=data['ranking'])
    if rank:
        return jsonify({'message': 'Rank updated successfully'}), 200
    else:
        return jsonify({'error': 'Rank not updated'}), 400
    
@rank_views.route('/api/rank/points', methods=['PUT'])
@admin_required
def api_update_rank_points():
    data = request.json
    rank = update_rank_points(competitor_id=data["competitor_id"] , points=data['points'])
    if rank:
        return jsonify({'message': 'Rank points updated successfully'}), 200
    else:
        return jsonify({'error': 'Rank point not updated'}), 400