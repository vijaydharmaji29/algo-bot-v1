import math

class action(object):
    def __init__(self, ticker, buy, sell, buy_val, sell_val):
        self.ticker = ticker
        self.buy = buy
        self.sell = sell
        self.buy_val = buy_val
        self.sell_val = sell_val

    def show(self):
        print(self.ticker, self.buy,
              self.sell, self.buy_val, self.sell_val)

    def __str__(self):
        to_show = "{} {} {} {} {}".format(self.ticker, self.buy, self.buy_val, self.sell, self.sell_val)
        return to_show

def next(stocks, positions, capital):
    # print(positions.index)
    positions['action'] = 0
    sorted_stocks = stocks.sort_values('Momentum')
    sorted_stocks = sorted_stocks[:10] #slicing top 10 momentum stocks

    execute = []
    x = capital*0.9 * math.pow(2,10)/(math.pow(2,11) - 2)

    #figuring out long positions
    i = 0
    for ticker, row in sorted_stocks.iterrows():

        if (ticker not in positions.index) and row["20_ma"] > row["200_ma"]:
            buy_val = x / (math.pow(2, i + 1))
            new_action = action(ticker, True, False, buy_val, 0)
            execute.append(new_action)
            row['action'] = 1
            i+=1

    #figuring out short positions:
    for ticker, row in positions.iterrows():
        if (ticker not in sorted_stocks.index) and (row["100_ma"] > row["Close"] or row['rsi'] < 30) and row["20_ma"] < row["200_ma"]:
            # short
            new_action = action(ticker, False, True, 0, row['Close'])
            execute.append(new_action)
            row['action'] = 2

    return execute
