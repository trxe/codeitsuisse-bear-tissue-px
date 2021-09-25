import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

def parse(data):
    cases = [Case(i['energy'], i['capital'], i['timeline']) for i in data]
    return cases

def earn(firm, buy, sell) -> int:
    return firm[buy].qty * (firm[sell].price - firm[buy].price)

def check(name, case, max_energy): 
    firm = case.filter(name)
    size = len(firm)
    if (size < 1):
        return 0
    buy = 0
    sell = 0 # max element
    max_diff = earn(firm, buy, sell)
    energy = 0
    for i in range(1, size):
        if energy > max_energy:
            return max_diff

        diff = earn(firm, i, sell)
        if (diff > max_diff):
            max_diff = diff
            buy = i
        if (firm[i].price > firm[sell].price):
            sell = i

    return max_diff


@app.route('/stonks', methods=['POST'])
def evaluateStonks():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    cases = parse(data)
    for case in cases:
        print(check("Apple", case, case.energy))
    return json.dumps(3)

# CLASS DEFINITIONS
class Case:
    def __init__(self, energy, capital, timeline) -> None:
        self.energy = energy
        self.capital = capital
        self.timeline = timeline
    
    def __repr__(self) -> str:
        return str(self.energy) + " " + str(self.capital) + " " + str(self.timeline)
    
    def toJSON(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def filter(self, stock_name) -> dict:
        out = []
        for year_num in self.timeline:
            year = self.timeline[year_num]
            if year[stock_name] != None:
                out.append(Stock(year[stock_name], stock_name, year_num))
        out.sort(key=lambda x: x.year, reverse=True)
        return out

class Stock:
    def __init__(self, raw, name, year) -> None:
        self.name = name
        self.year = int(year)
        self.price = raw['price']
        self.qty = raw['qty']
    
    def __repr__(self) -> str:
        return "{" + self.name + ": " + str(self.year) + " | "  + str(self.price) + " | " + str(self.qty) + "}"
    
    def toJSON(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
