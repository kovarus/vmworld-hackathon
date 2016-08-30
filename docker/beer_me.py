#!/usr/bin/env python3
from flask import Flask, jsonify, make_response

import uuid

# Initiate Flask
app = Flask(__name__)

# Generate a "short" uuid for this instance
uid = str(uuid.uuid4())[:8]

@app.route('/api/beer', methods=['GET'])
def get_some():

    print ("Getting someone some beer...")

    payload = {
        "Cost": "Free",
        "Temp": "Cold",
        "Brand": "Who Cares?",
		"Node": uid
    }
    return jsonify(payload)

@app.errorhandler(404)
@app.errorhandler(405)
def not_found(error_code):
    return make_response(jsonify({'error': 'Not Found'}), str(error_code))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
