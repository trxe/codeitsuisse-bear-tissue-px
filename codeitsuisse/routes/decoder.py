import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/decoder', methods=['POST'])
def evaluateDecoder():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    input = data.get("input")
    values = input['possible_values']
    num_slots = input['num_slots']
    history = input['history']
    result = None

    logging.info("My result :{}".format(result))
    return json.dumps(result)



