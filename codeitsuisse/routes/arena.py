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
initial = None
myId = "O"

grid = {
    'NW': '-', 
    'N': '-', 
    'NE': '-', 
    'W': '-', 
    'C': '-', 
    'E': '-', 
    'SW': '-', 
    'S': '-', 
    'SE': '-', 
}

def isValid(loc, player):
    if not loc in grid:
        return False
    if grid[loc] != '-':
        return False
    return True

@app.route('/tic-tac-toe', methods=['POST'])
def evaluateArena():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    battleId = data.get("battleId")
    URL = "https://cis2021-arena.herokuapp.com/tic-tac-toe/start/" + battleId 
    print(URL)
    messages = SSEClient(URL)
    for msg in messages:
        if initial == None:
            initial = json.loads(msg)
            myId = initial['youAre']
            print(myId)
        else:
            action = json.loads(msg)
            if (action['action'] != 'putSymbol'):
                continue
            print(msg)
            loc = msg['position']
            player = msg['player']
            if isValid(loc, player):
                print("valid")
                grid[loc] = player
                requests.post(URL, data=payload)
            else:
                print("invalid")
                requests.post(URL, data=invalid)
        time.sleep(1.0)

    return json.dumps(invalid)