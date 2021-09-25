import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/stig/perry', methods=['POST'])
def evaluateStig1():
    data = request.get_json()
    for i in data:
        print(i["coefficients"])
        print(i["maxRating"])
        print(i["question"][0])
    return json.dumps(None)