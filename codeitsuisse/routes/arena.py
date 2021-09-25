import logging
import json
import requests
import queue
import time

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
    test = requests.get(url=URL).json()
    print(test)
    '''
    print(test)
    generator = stream(URL)
    for msg in generator:
        print(msg)
        time.sleep(1.0)
    '''

    return json.dumps(payload)

def get_message(URL):
    '''this could be any function that blocks until data is ready'''
    requests.get(url=URL)
    time.sleep(1.0)
    s = time.ctime(time.time())
    return s

def stream(URL):
    def eventStream():
        while True:
            # wait for source data to be available, then push it
            yield 'data: {}\n\n'.format(get_message(URL))
    return Response(eventStream(), mimetype="text/event-stream")
