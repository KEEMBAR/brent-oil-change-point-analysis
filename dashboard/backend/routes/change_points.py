# dashboard/Backend/routes/changepoints.py

from flask import Blueprint, jsonify
import pandas as pd
import os

bp = Blueprint('changepoints', __name__, url_prefix='/api')

# Load changepoints data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, '../../../data/changepoints.csv')
changepoints_data = pd.read_csv(data_path, parse_dates=['Date'])

@bp.route('/changepoints', methods=['GET'])
def get_changepoints():
    changepoints_data['Date'] = changepoints_data['Date'].dt.strftime('%Y-%m-%d')
    return jsonify(changepoints_data.to_dict(orient='records'))
