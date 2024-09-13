from flask import Flask, jsonify, request
from uuid import uuid4

import os

app = Flask(__name__)

# Sample data
trades = [
    {
        "tradeId": "1",
        "country": {"name": "USA"},
        "energyProvider": {"name": "ExxonMobil"},
        "quantity": 1000,
        "price": 50.00,
        "trackingInformation": "Shipped via pipeline"
    },
    {
        "tradeId": "2",
        "country": {"name": "Canada"},
        "energyProvider": {"name": "Suncor Energy"},
        "quantity": 500,
        "price": 45.00,
        "trackingInformation": "Delivered by truck"
    }
]

# Error response schema
error_schema = {
    "errorMessage": "An error occurred."
}

# Trade schema
trade_schema = {
    "tradeId": str,
    "country": {"name": str},
    "energyProvider": {"name": str},
    "quantity": int,
    "price": float,
    "trackingInformation": str
}

# Authentication (placeholder - replace with actual authentication)
def authenticate(token):
    # Replace with your actual authentication logic
    if token:
        return True
    else:
      return False

# GET /trades
@app.route('/trades', methods=['GET'])
def get_trades():
    if not authenticate(request.headers.get('Authorization')):
        return jsonify(error_schema), 401
    return jsonify(trades), 200

# POST /trades
@app.route('/trades', methods=['POST'])
def create_trade():
    if not authenticate(request.headers.get('Authorization')):
        return jsonify(error_schema), 401
    data = request.get_json()
    if not all(key in data for key in trade_schema.keys()):
        return jsonify(error_schema), 400
    new_trade = {
        "tradeId": str(uuid4()),
        **data
    }
    trades.append(new_trade)
    return jsonify(new_trade), 200

# GET /trades/{tradeId}
@app.route('/trades/<tradeId>', methods=['GET'])
def get_trade(tradeId):
    if not authenticate(request.headers.get('Authorization')):
        return jsonify(error_schema), 401
    for trade in trades:
        if trade['tradeId'] == tradeId:
            return jsonify(trade), 200
    return jsonify(error_schema), 404

# PUT /trades/{tradeId}
@app.route('/trades/<tradeId>', methods=['PUT'])
def update_trade(tradeId):
    if not authenticate(request.headers.get('Authorization')):
        return jsonify(error_schema), 401
    data = request.get_json()
    if not all(key in data for key in trade_schema.keys()):
        return jsonify(error_schema), 400
    for i, trade in enumerate(trades):
        if trade['tradeId'] == tradeId:
            trades[i] = {
                "tradeId": tradeId,
                **data
            }
            return jsonify(trades[i]), 200
    return jsonify(error_schema), 404

# DELETE /trades/{tradeId}
@app.route('/trades/<tradeId>', methods=['DELETE'])
def delete_trade(tradeId):
    if not authenticate(request.headers.get('Authorization')):
        return jsonify(error_schema), 401
    for i, trade in enumerate(trades):
        if trade['tradeId'] == tradeId:
            del trades[i]
            return jsonify({"message": "Trade deleted successfully."}), 200
    return jsonify(error_schema), 404

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
