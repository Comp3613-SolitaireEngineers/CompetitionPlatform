from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required
from App.controllers import *


competitor_views = Blueprint('competitor_views', __name__, template_folder='../templates')


@competitor_views.route('/api/competitors', methods=['GET'])
def api_get_competitors():
    competitors = get_all_competitors_json()
    if competitors:
        return (jsonify(competitors),200)
    return jsonify({'message': 'No Competitors found'}), 405


@competitor_views.route('/api/competitor', methods=['POST'])
def api_add_new_competitor():    
    data = request.json
    competitor = create_competitor(data['username'], data['password'])
    
    if competitor:
        return jsonify({'message': 'Competitor created successfully'}), 201
    else:
        return jsonify({'error': 'Competitor not created'}), 400
    
@competitor_views.route('/api/competitor/<id>', methods=['GET'])
def api_get_competitor_by_id(id):
    competitor = get_competitor_by_id(id)
    if competitor:
        return jsonify(competitor.get_json()), 200
    return jsonify({'message': 'No Competitor found'}), 405