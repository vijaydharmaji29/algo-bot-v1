import yfinance as yf
import numpy as np
from scipy.stats import linregress
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


global final_data

def calculate_momentum(data, period):
    close = np.array(data.Close)
    momentums = []

    for i in range(len(close)):
        if i < period:
            momentums.append(None)
            continue

        y_data = np.log(close[i-period: i])
        x_data = np.arange(period)
        beta, _, rvalue, _, _ = linregress(x_data, y_data)
        momentums.append(((1 + beta) ** 252) * (rvalue ** 2))

    data['Momentum'] = momentums


def ticker_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period='1y', interval='60m', auto_adjust = True) #data is pandas data frame

    calculate_momentum(data, 90)
    data["20_ma"] = data["Close"].ewm(span=20).mean()
    data["200_ma"] = data["Close"].ewm(span=200).mean()
    data["100_ma"] = data["Close"].ewm(span=20).mean()
    data['move'] = data['Close'] - data['Close'].shift(1)
    data['up'] = np.where(data['move'] > 0, data['move'], 0)
    data['down'] = np.where(data['move'] < 0, data['move'], 0)
    data['average_gain'] = data['up'].rolling(14).mean()
    data['average_loss'] = data['down'].abs().rolling(14).mean()
    relative_strength = data['average_gain'] / data['average_loss']
    data['rsi'] = 100.0 - (100.0 / (1.0 + relative_strength))

    data = data.dropna()

    return data #returning a pandas dataframe

def calc_momentum(close):
    period = 90

    y_data = np.log(close[- period:])
    x_data = np.arange(period)
    beta, _, rvalue, _, _ = linregress(x_data, y_data)
    momentum = ((1 + beta) ** 252) * (rvalue ** 2)

    return momentum

def calculate_average_gain(move, past_move, period):
    gain = move
    ctr = 0

    for i in range(-period, 0):
        gain += past_move[i]
        ctr += 1

    return gain/ctr

def calculate_average_loss(move, past_move, period):
    loss = move
    ctr = 0

    for i in range(-period, 0):
        loss += past_move[i]
        ctr += 1

    return abs(loss)/ctr

def calculate_ma(recent, past_data, period):
    multiplier = 2/(period+1)
    p = str(period) + '_ma'
    ema = (recent['Close']*multiplier) + past_data[p][-1]*(1-multiplier)

    return ema

class recent_session_obj():

    def __init__(self, recent, past_data):
        self.recent = recent
        self.past_data = past_data

        self.close = self.past_data['Close']
        self.close.append(pd.Series(self.recent['Close']), ignore_index=True)

        self.momentum = calc_momentum(self.close)
        self.ma_20 = calculate_ma(self.recent, self.past_data, 20)
        self.ma_200 = calculate_ma(self.recent, self.past_data, 200)
        self.ma_100 = calculate_ma(self.recent, self.past_data, 100)

        self.move = self.close[-1] - self.close[-2]
        self.up = self.move if self.move > 0 else 0
        self.down = self.move if self.move < 0 else 0

        self.average_gain = calculate_average_gain(self.move, self.past_data['up'], 14)
        self.average_loss = calculate_average_loss(self.move, self.past_data['down'], 14)

        self.relative_strength = self.average_gain/self.average_loss
        self.rsi = 100.0 - (100.0 / (1.0 + self.relative_strength))


def recent_session(ticker, past_data):
    stock = yf.Ticker(ticker)
    data = stock.history(period='1d', interval='60m', auto_adjust=True)  # data is pandas data frame
    recent = data.iloc[-1]

    rs = recent_session_obj(recent, past_data)

    recent = pd.Series(recent)

    recent['Momentum'] = rs.momentum
    recent["20_ma"] = rs.ma_20
    recent["200_ma"] = rs.ma_200
    recent["100_ma"] = rs.ma_100
    recent['move'] = rs.move
    recent['up'] = rs.up
    recent['down'] = rs.down
    recent['average_gain'] = rs.average_gain
    recent['average_loss'] = rs.average_loss
    recent['rsi'] = rs.rsi

    # print(type(past_data), type(past_data['Close']), type(recent), type(recent['Close']))

    return recent #recent is a pandas series

if __name__ == '__main__':
    past_data = ticker_data('MSFT')
    recent = recent_session('MSFT', past_data)

    print(recent.info)