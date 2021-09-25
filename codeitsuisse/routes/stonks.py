import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)
INF = 10000000

# CLASS DEFINITIONS
class Case:
    def __init__(self, energy, capital, timeline) -> None:
        self.energy = energy
        self.capital = capital
        self.timeline = [Year(timeline[y], y) for y in timeline]
    
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

class Year:
    def __init__(self, stocks, year) -> None:
        self.year = int(year)
        self.stocks = {name:Stock(details, name, year) for (name,details) in stocks.items()}

    def __repr__(self) -> str:
        return ">" + str(self.year) + ": " + str(self.stocks)

class Stock:
    def __init__(self, raw, name, year) -> None:
        self.name = name
        self.year = int(year)
        self.price = raw['price']
        self.qty = raw['qty']
    
    def __repr__(self) -> str:
        return "{" + self.name + ": " + str(self.year) + " | "  + str(self.price) + " | " + str(self.qty) + "}"

class Firm:
    def __init__(self, stock) -> None:
        # list of trades (buy, sell)
        self.trades = [];
        self.curr = (None, stock)
        self.curr_price = (stock.price, stock.price)

    def curr_buy_price(self) -> int:
        return self.curr_price[0];

    def curr_sell_price(self) -> int:
        return self.curr_price[1];
    
    def set_buy(self):
        pass


def parse(data):
    cases = [Case(i['energy'], i['capital'], i['timeline']) for i in data]
    return cases

def earn(firm, buy, sell) -> int:
    return firm[buy].qty * (firm[sell].price - firm[buy].price)

def check(case):
    max_en = case.energy / 2
    en = 0
    timeline = case.timeline
    size = len(timeline)
    db = {name : None for (name, stock) in timeline[0].stocks.items()}
    print(db)

@app.route('/stonks', methods=['POST'])
def evaluateStonks():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    cases = parse(data)
    for case in cases:
        check(case)
        # print(check("Apple", case, case.energy))
    return json.dumps(3)
