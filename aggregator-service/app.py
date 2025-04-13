from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

# Simulate sales data
sales_data = [
    {"team": "A", "product": "Life Plan", "branch": "Colombo", "sales": 120},
    {"team": "B", "product": "Health Plan", "branch": "Kandy", "sales": 150},
    {"team": "A", "product": "Health Plan", "branch": "Colombo", "sales": 180}
]

@app.route('/aggregate', methods=['GET'])
def aggregate():
    results = {
        "top_team": max(sales_data, key=lambda x: x['sales'])['team'],
        "top_product": max(sales_data, key=lambda x: x['sales'])['product'],
        "timestamp": datetime.utcnow().isoformat()
    }
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')