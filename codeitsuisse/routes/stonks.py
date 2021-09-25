import logging
import json

from flask import request, jsonify

from codeitsuisse import app
# from stonks.case import Case

logger = logging.getLogger(__name__)

@app.route('/stonks', methods=['POST'])
def evaluateStonks():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    print(data[0])
    # inputValue = data.get("input")
    # result = inputValue * inputValue
    # logging.info("My result :{}".format(result))
    return json.dumps(3) #json.dumps(result)

def parse(data):
    out = json.loads(data)
    #out_dict = [Case(i['energy'], i['capital'], i['timeline']) for i in out]
    return out # out_dict