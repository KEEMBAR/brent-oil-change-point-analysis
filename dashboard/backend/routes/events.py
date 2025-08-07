# dashboard/Backend/routes/events.py

from flask import Blueprint, jsonify
import pandas as pd
import os

bp = Blueprint('events', __name__, url_prefix='/api')

# Load events data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
events_path = os.path.join(BASE_DIR, '../../../data/events.csv')
events_data = pd.read_csv(events_path, parse_dates=['date'])

@bp.route('/events', methods=['GET'])
def get_events():
    events_data['date'] = events_data['date'].dt.strftime('%Y-%m-%d')
    return jsonify(events_data.to_dict(orient='records'))
