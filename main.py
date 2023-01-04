import pandas as pd
import setup
import stock_data as sd
import numpy as np
import brain
import time
import broker
import executioner

def act():
    global stock_data
    global positions

    print('BASIC DATA')
    capital = 100000
    stock_data, positions = setup.setup(capital, 'nifty50')
    print('FINISHED SETTING UP')

    while True:
        print('TRADING...')
        positions = broker.get_positions()
        capital = broker.get_capital()
        recent_session = next()
        actions = brain.next(recent_session, positions, capital)
        print(actions)
        executioner.trade(actions)
        print('ACTIONS EXECUTED...')

        time.sleep(60)



def next():
    data = {
        'Open': [],
        'High': [], 'Low': [],
        'Close': [], 'Volume': [],
        'Dividends': [], 'Stock Splits': [],
        'Momentum': [], '20_ma': [],
        '200_ma': [], '100_ma': [],
        'move': [], 'up': [],
        'down': [], 'average_gain': [],
        'average_loss': [], 'rsi': []
    }
    recent_session = pd.DataFrame(data)

    for ticker in stock_data.keys():
        recent_session.loc[ticker] = np.array(sd.recent_session(ticker, stock_data[ticker]))

    return recent_session

if __name__ == '__main__':
    act()

