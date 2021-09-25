import logging
import json
import requests
import time
from sseclient import SSEClient

from flask import request, jsonify, Response, render_template, Flask

from codeitsuisse import app

logger = logging.getLogger(__name__)
payload = { "action": "putSymbol", "position": "SE" }
invalid = { "action": "(╯°□°)╯︵ ┻━┻" }

@app.route('/tic-tac-toe', methods=['POST'])
def evaluateArena():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    battleId = data.get("battleId")
    URL = "https://cis2021-arena.herokuapp.com/tic-tac-toe/start/" + battleId 
    print(URL)
    messages = SSEClient(URL)
    for msg in messages:
        print(msg)
        time.sleep(1.0)

    return json.dumps(payload)