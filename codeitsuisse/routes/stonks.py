import logging
import json

from flask import request, jsonify

from codeitsuisse import app
from .Stonks.case import Case

logger = logging.getLogger(__name__)

def parse(data):
    cases = [Case(i['energy'], i['capital'], i['timeline']) for i in data]
    return cases

@app.route('/stonks', methods=['POST'])
def evaluateStonks():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    cases = parse(data)
    for case in cases:
        print(case)
    # inputValue = data.get("input")
    # result = inputValue * inputValue
    # logging.info("My result :{}".format(result))
    return cases[0].toJSON() #json.dumps(result)