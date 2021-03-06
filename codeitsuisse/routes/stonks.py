from datetime import time
import logging
import json

from flask import request, jsonify, Response

from codeitsuisse import app

logger = logging.getLogger(__name__)

class Case:
    def __init__(self, energy, capital, timeline) -> None:
        self.energy = energy
        self.capital = capital
        self.timeline = [(int(year), stocks) for (year,stocks) in timeline.items()]
    
    def __repr__(self) -> str:
        return "energy: {},\ncapital: {},\ntimeline: {}".format(self.energy, self.capital, self.timeline)
    
    def toJSON(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
class Trade:
    def __init__(self, buy, sell) -> None:
        self.buy = buy
        self.sell = sell

    def year_start(self) -> int:
        return self.buy['year']
    
    def __eq__(self, other) -> bool:
        return self.buy == other.buy and self.sell == other.sell
    
    def compare(self, other) -> int:
        return self.buy['year'] - other.buy['year']

    def __repr__(self) -> str:
        return "buy: {}, sell: {}".format(self.buy, self.sell)
    
    def __hash__(self) -> int:
        return hash(self.__repr__())

class Firm:
    def __init__(self) -> None:
        self.curr_min = {"price": 10000000}
        self.curr_max = {"price": 0}
        self.trades = []
    
    def set_min(self, info, year) -> None:
        info['year'] = year
        self.curr_min = info

    def set_max(self, info, year) -> None:
        info['year'] = year
        self.curr_max = info
    
    def compare_min(self, info) -> int:
        return self.curr_min['price'] - info['price']
    
    def compare_max(self, info) -> int:
        return self.curr_max['price'] - info['price']

    def add_trade(self) -> tuple:
        if self.curr_min['price'] >= self.curr_max['price']:
            return None
        if self.curr_min['year'] >= self.curr_max['year']:
            return None
        t = Trade(self.curr_min, self.curr_max)
        self.trades.append(t)
        return t

    def __repr__(self) -> str:
        return "min: {}, max: {}, trades: {}".format(self.curr_min, self.curr_max, self.trades)

def parse(data) -> list:
    cases = [Case(i['energy'], i['capital'], i['timeline']) for i in data]
    return cases

def getAllFirms(timeline, firms) -> dict:
    if len(timeline) <= 0:
        return firms
    new_firms = {name : Firm() for name in timeline[0][1]}
    firms.update(new_firms)
    return getAllFirms(timeline[1:], firms)

def track_all(energy, timeline, firms):
    if len(timeline) == 0 or energy < 0:
        return
    year_num = timeline[0][0]
    this_year = timeline[0][1]
    for (name, firm) in firms.items():
        if name in this_year:
            firm.set_max(this_year[name], year_num)
    track(energy, timeline[1:], firms, timeline[0][0])

# gets the list of peaks and troughs
def track(energy, timeline, firms, year):
    if len(timeline) == 0 or energy < 0:
        return
    year_num = timeline[0][0]
    this_year = timeline[0][1]
    for (name, firm) in firms.items():
        if not name in this_year:
            continue
        if firm.compare_max(this_year[name]) < 0:
            firm.set_max(this_year[name], year_num)
        if firm.compare_min(this_year[name]) > 0:
            firm.set_min(this_year[name], year_num)
        else:
            firm.add_trade()
        if len(timeline) == 1:
            firm.add_trade()
    track(energy - (year - year_num), timeline[1:], firms, year_num)

def earn(pair, capital, name):
    buy = pair.buy
    sell = pair.sell
    qty = (capital - capital % buy['price']) / buy['price']
    if qty == 0:
        return 0, [], 0
    val = qty * (sell['price'] - buy['price'])
    log = ["j-{}-{}".format(sell['year'], buy['year']), "b-{}-{}".format(name, qty)]
    log.extend(["j-{}-{}".format(buy['year'], sell['year']), "s-{}-{}".format(name, qty)])
    return qty*buy['price'], log, val

@app.route('/stonks', methods=['POST'])
def evaluateStonks():
    data = request.get_json()
    cases = parse(data)
    print(data)

    all_actions = []
    for case in cases:
        print("new case")
        actions = []
        firms = getAllFirms(case.timeline, {})
        track_all(case.energy / 2, case.timeline, firms)
        for (f, firm) in firms.items():
            firm.trades = list(dict.fromkeys(firm.trades))
            for c in firm.trades:
                print(f, c)
                cost, action, profit = earn(c, case.capital, f)
                if profit != 0 and cost <= case.capital: 
                    case.capital -= cost
                    actions.extend(action)
        all_actions.append(actions)
    return Response(json.dumps(all_actions), mimetype="application/json")