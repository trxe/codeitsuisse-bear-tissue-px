import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/decoder', methods=['POST'])
def evaluateDecoder():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    values = data["possible_values"]
    num_slots = data["num_slots"]
    history = data["history"]
    print(values)
    print(num_slots)
    for h in history:
        print(h)
    guess = [2, 2, 2, 4, 4]
    guess = [values[i] for i in guess]
    #guess = ['s', 'x', 's', 'b', 'b']

    logging.info("My guess :{}".format(guess))
    return json.dumps({"answer" : guess})