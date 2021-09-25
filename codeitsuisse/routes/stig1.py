import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/stig/perry', methods=['POST'])
def evaluateStig1():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    for i in data:
        print(i)
    return json.dumps(None)