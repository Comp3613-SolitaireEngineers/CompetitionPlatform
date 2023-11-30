from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('leaderboard.html')

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()    
    return jsonify(message='The Database has been successfully initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})

@index_views.route('/healthcheck', methods=['GET'])
def health():
    return jsonify({'status':'healthy'})


@index_views.route('/leaderboard', methods=['GET'])
def leaderboard():
    return render_template('leaderboard.html')