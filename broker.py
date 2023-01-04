import csv
import yfinance as yf
import numpy as np
import pandas as pd

def get_price(ticker):
    return (yf.Ticker(ticker).info['currentPrice'])

def update_positions(ticker, action, number=0, buy_val=0):
    p = []

    with open('positions.csv', mode='r') as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            p.append(lines)

    if not action:
        number = 0
        c = 0
        for i in range(len(p)):
            if p[i][0] == ticker:
                number = p[i][1]
                c = i
                break
        p.pop(c)

    else:
        p.append([ticker, number, buy_val])

    with open('positions.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(p)

    return number


def get_capital():
    capital = 0
    with open('capital.txt') as f:
        contents = f.read()
        capital = float(contents)

    return capital

def update_capital(capital):
    with open('capital.txt', 'w') as f: #updated by broker later on
        f.write(str(capital))

def get_positions():
    p = []
    with open('positions.csv', mode='r') as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            p.append(lines)

    if p:
        positions = pd.DataFrame(np.array(p), columns=['ticker', 'price_per_share', 'number'])
    else:
        positions = pd.DataFrame(columns=['ticker', 'price_per_share', 'number'])

    positions = positions.set_index('ticker')

    return positions

def buy(ticker, number):
    capital = get_capital()
    price = get_price(ticker)
    capital -= number*price

    update_capital(capital)
    update_positions(ticker, True, number, price)

    print('BOUGHT -', ticker, '-', number)




def sell(ticker):
    #check how many of it is there
    #and sell all
    #update positions
    #update capital
    capital = get_capital()
    price = get_price(ticker)

    update_capital(capital)
    number = update_positions(ticker, False)
    capital += number*price
    print('SOLD -', ticker, '-', number)

if __name__ == '__main__':
    msft = yf.Ticker("TSLA")

    # get stock info
    print(msft.info['currentPrice'])