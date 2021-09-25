import logging
import json
import requests

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/arena', methods=['POST'])
def evaluateArena():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    battleId = data.get("battleId")
    print(battleId)
    #print(get_data(battleId))

    logging.info("My result :{}".format(battleId))
    return json.dumps(battleId)

def get_data(battleId):
    return requests.get("https://cis2021-arena.herokuapp.com/tic-tac-toe/start/" + battleId).content

