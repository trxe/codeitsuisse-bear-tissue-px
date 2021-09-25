import logging
import json
import requests

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
    print(history)
    guess = values[0:num_slots]
    input = json.dumps({"answer" : guess})
    #output = {"output_received": None, "result" : 0}
    requests.post(input)
    output = request.get_json()
    print(output)

    logging.info("My guess :{}".format(guess))
    return input