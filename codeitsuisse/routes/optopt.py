import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/optopt', methods=['POST'])
def evaluateOptOpt():
    data = request.get_json()
    print(data)
    logging.info("data sent for evaluation {}".format(data))
    return json.dumps(None)



