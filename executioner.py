import broker
import math

def trade(actions):
    for a in actions:
        print(a)
        if a.buy and not a.sell:
            ticker_price = broker.get_price(a.ticker)
            number = math.floor(a.buy_val / ticker_price)
            print(number)
            if number != 0:
                r = broker.buy(a.ticker, number)
                print('BUYING')

        if a.sell and not a.buy:
            r = broker.sell(a.ticker)
            print('SELLING')

