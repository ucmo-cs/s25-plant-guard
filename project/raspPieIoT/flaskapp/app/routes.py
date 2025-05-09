from flask import Blueprint, render_template, jsonify
from app.sensors import read_sensors

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')
    
@main.route('/data')
def data():
    return jsonify(read_sensors())
