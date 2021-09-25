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

def isValid(grid, loc, player):
    if not loc in grid:
        return False
    if grid[loc] != '-':
        return False
    return True

def make_request(reply, URL) -> bool:
    result = requests.post(URL, data=reply, timeout=3.0)
    if result.status_code == requests.codes.ok: 
        print("ok liao")
        return True
    else:
        print(result.status_code, result.reason)
        return False


@app.route('/tic-tac-toe', methods=['POST'])
def evaluateArena():
    global payload, invalid
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
    initial = None
    myId = "O"

    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    battleId = data.get("battleId")
    URL = "https://cis2021-arena.herokuapp.com/tic-tac-toe/start/" + battleId 
    print(URL)
    messages = SSEClient(URL)
    for msg in messages:
        if initial == None:
            initial = json.loads(msg.__str__())
            print(initial)
            myId = initial['youAre']
            print(myId)
            if (myId == 'O'):
                if not make_request(payload, URL):
                    print("init failed")
                    return json.dumps(None)
        else:
            action = json.loads(msg.__str__())
            if (action['action'] != 'putSymbol'):
                return json.dumps(None)
            print(action)
            loc = action['position']
            player = action['player']
            if isValid(grid, loc, player):
                print("valid")
                grid[loc] = player
                if not make_request(payload, URL):
                    return json.dumps(None)
            else:
                print("invalid")
                if not make_request(invalid, URL):
                    return json.dumps(None)
        time.sleep(1.0)

    return json.dumps(None)