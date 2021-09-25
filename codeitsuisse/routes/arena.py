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
    result = requests.post(URL, data=reply)
    if result.status_code == requests.codes.ok: 
        return True
    else:
        print(result.status_code, result.reason)
        return False

def modify_position(loc, payload, grid):
    if loc == payload['posiition']:
        for pos in grid:
            if grid['pos'] == '-':
                payload['position'] = pos
                break


def print_grid(grid):
    output = '{} {} {}\n{} {} {}\n{} {} {}'.format(grid['NW'], grid['W'], grid['NE'], grid['W'], grid['C'], grid['E'], grid['SW'], grid['S'], grid['SE'])
    print(output)


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
    myId = 'O'

    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    battleId = data.get("battleId")
    URLstart = "https://cis2021-arena.herokuapp.com/tic-tac-toe/start/" + battleId 
    print(URLstart)
    URLplay = "https://cis2021-arena.herokuapp.com/tic-tac-toe/play/" + battleId 
    messages = SSEClient(URLstart)
    for msg in messages:
        if initial == None:
            initial = json.loads(msg.__str__())
            myId = initial['youAre']
            print(myId)
            if (myId != 'O'):
                if not make_request(payload, URLplay):
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
                grid[loc] = player
                modify_position(loc, payload, grid)
                if not make_request(payload, URLplay):
                    print("valid reply failed")
                    return json.dumps(None)
            else:
                if not make_request(invalid, URLplay):
                    print("invalid reply failed")
                    return json.dumps(None)
        time.sleep(1.0)

    return json.dumps(None)
