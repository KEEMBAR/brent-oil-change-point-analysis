import os
import pandas as pd
from flask import Flask, jsonify
from flask_cors import CORS

from routes.prices import bp as prices_bp
from routes.events import bp as events_bp
from routes.change_points import bp as changepoints_bp

app = Flask(__name__)
CORS(app)

# Register all blueprints
app.register_blueprint(prices_bp)
app.register_blueprint(events_bp)
app.register_blueprint(changepoints_bp)

# Helper: get absolute path to the parent directory of Backend/
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

@app.route('/api/summary', methods=['GET'])
def get_summary():
    prices_path = os.path.join(BASE_DIR, '../../data/raw/BrentOilPrices.csv')
    events_path = os.path.join(BASE_DIR, '../../data/events.csv')
    changepoints_path = os.path.join(BASE_DIR, '../../data/changepoints.csv')

    prices = pd.read_csv(prices_path)
    events = pd.read_csv(events_path)
    changepoints = pd.read_csv(changepoints_path)
    
    summary = {
        'overall_mean_price': round(prices['Price'].mean(), 2),
        'num_events': len(events),
        'num_changepoints': len(changepoints),
    }
    return jsonify(summary)

if __name__ == '__main__':
    app.run(debug=True)
