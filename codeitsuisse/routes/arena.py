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
    response = stream(URL)
    print(response)

    return json.dumps(payload)

def get_message():
    '''this could be any function that blocks until data is ready'''
    time.sleep(1.0)
    s = time.ctime(time.time())
    return s

def stream(URL):
    def eventStream():
        # messages = requests.get(URL)
        test = requests.get(URL)
        print("eventstream", requests.get(URL))
        while True:
            get_message()
            # wait for source data to be available, then push it
            yield 'data: {}\n\n'.format(test)
    return Response(eventStream(), mimetype="text/event-stream")
