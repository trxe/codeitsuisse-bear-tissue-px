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
end_game = json.dumps(None)

def is_valid(grid, loc, player):
    if not loc in grid:
        return False
    if grid[loc] != '-':
        return False
    return True

def make_post(reply, URL) -> bool:
    result = requests.post(URL, data=reply)
    if result.status_code == requests.codes.ok: 
        return True
    else:
        print(result.status_code, result.reason)
        return False

def modify_position(payload, grid):
    for pos in grid:
        if grid[pos] == '-':
            payload['position'] = pos
            break

def print_grid(grid):
    output = '{} {} {}\n{} {} {}\n{} {} {}'.format(grid['NW'], grid['W'], grid['NE'], grid['W'], grid['C'], grid['E'], grid['SW'], grid['S'], grid['SE'])
    print(output)

@app.route('/tic-tac-toe', methods=['POST'])
def evaluateArena():
    global payload, invalid, end_game
    grid = { 'NW': '-', 'N': '-', 'NE': '-', 
    'W': '-', 'C': '-', 'E': '-', 
    'SW': '-', 'S': '-', 'SE': '-', }
    myId = 'O'
    print_grid(grid)

    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    battleId = data.get("battleId")
    URLstart = "https://cis2021-arena.herokuapp.com/tic-tac-toe/start/" + battleId 
    URLplay = "https://cis2021-arena.herokuapp.com/tic-tac-toe/play/" + battleId 
    print(URLstart)
    messages = SSEClient(URLstart)
    for rawmsg in messages:
        msg = json.loads(rawmsg.__str__())
        print(msg)
        if 'youAre' in msg:
            myId = msg['youAre']
            print(myId)
            if (myId != 'O'):
                if not make_post(payload, URLplay):
                    print("init failed")
                    return end_game
            continue
        elif 'winner' in msg:
            return end_game
        elif not 'action' in msg:
            make_post(invalid, URLplay)
        else: # player in message
            # they flipped me
            if msg['action'] != 'putSymbol':
                print("you flipped me")
                return end_game
            loc = msg['position']
            player = msg['player']
            if is_valid(grid, loc, player):
                grid[loc] = player
                if not is_valid(grid, payload['position'], myId):
                    modify_position(payload, grid)
                grid[payload['position']] = myId
                make_post(payload, URLplay)
            else:
                make_post(invalid, URLplay)
        time.sleep(1.0)
        print_grid(grid)

    return end_game
