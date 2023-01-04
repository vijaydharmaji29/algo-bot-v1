#runs only once when the program is first setup\
import pandas as pd
import csv
import broker

import stock_data as sd

def setup(capital, filename):
    with open('capital.txt', 'w') as f: #updated by broker later on
        f.write(str(capital))

    with open('positions.csv', 'w') as f: #updated by broker later on
        pass

    #call broker to update positions.csv
    #broker.updatepositions()

    positions_data = {'ticker': [], 'number': [], 'buy_val': []}

    with open('positions.csv', 'r') as file:
        #create pandas dataframe with each row of positions
        csvreader = csv.reader(file)
        for row in csvreader:
            positions_data['ticker'].append(row[0])
            positions_data['number'].append(row[1])
            positions_data['buy_val'].append(row[2])

    positions = pd.DataFrame(positions_data)
    data = {}

    with open(filename) as f:
        lines = f.readlines()

        for i in lines:
            ticker_name = i[:-1]+'.NS'
            ticker_data = sd.ticker_data(ticker_name) #pandas dataframe
            data[ticker_name] = ticker_data

    return data, positions #dictionary of pandas dataframes, with index being tickers for that stock's data


if __name__ == '__main__':
    print(setup(10000, 'nifty50'))