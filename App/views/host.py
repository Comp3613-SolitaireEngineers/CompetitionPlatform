from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
# from flask_jwt_extended import jwt_required, current_user as jwt_current_user
# from flask_login import current_user, login_required

from App.controllers import *

host_views = Blueprint('host_views', __name__, template_folder='../templates')

@host_views.route('/api/host', methods=['POST'])
@admin_required
def api_create_host():
    data = request.json

    admin_id = data.get('admin_id')
    # host_id = data.get('id')
    name = data.get('name')
    website = data.get('website')

    if None in (admin_id, name, website):
        return jsonify({'error': 'Missing data in the request'}), 400
    
    if not (get_admin(admin_id)):
        return jsonify({'error': 'Admin not found'}), 404

    host = create_host(name=name, website=website)

    if host:
        return jsonify({'message': 'Host created successfully'}), 201
    else:
        return jsonify({'error': 'Host not created'}), 400
    

@host_views.route('/api/hosts', methods=['GET'])
def api_get_hosts():
    hosts = get_all_hosts_json()

    if not hosts:
        return jsonify({'message': 'No Hosts found'}), 404

    return jsonify(hosts), 200