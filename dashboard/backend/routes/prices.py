# dashboard/Backend/routes/prices.py

from flask import Blueprint, jsonify, request
import pandas as pd
import os

bp = Blueprint('prices', __name__, url_prefix='/api')

# Load Brent prices
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
price_path = os.path.join(BASE_DIR, '../../../data/raw/BrentOilPrices.csv')
brent_data = pd.read_csv(price_path, parse_dates=['Date'])

@bp.route('/prices', methods=['GET'])
def get_prices():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    filtered_data = brent_data.copy()

    if start_date:
        filtered_data = filtered_data[filtered_data['Date'] >= pd.to_datetime(start_date)]
    if end_date:
        filtered_data = filtered_data[filtered_data['Date'] <= pd.to_datetime(end_date)]

    filtered_data['Date'] = filtered_data['Date'].dt.strftime('%Y-%m-%d')
    return jsonify(filtered_data.to_dict(orient='records'))
