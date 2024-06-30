import pandas as pd
import numpy as np
from sklearn import linear_model


def find_trend(data, days=10):
    # if not data.empty():
        # find the trend for the past three days
    data1 = data.tail(days)
    data1['days_from_start'] = (data1.index - data1.index[0]).days
    x = data1['days_from_start'].values.reshape(-1, 1)
    y = data1['Adj Close'].values
    linear_model.LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)
    model = linear_model.LinearRegression().fit(x, y)
    slope = model.coef_
    print("Slope in this stock is :",slope)
    if abs(slope * 100) > 15:
        print("change in current share ",slope*100)
        return True
    else:
        return False


def find_ema(data, span=20):
    return data.values.ewm(span=span, adjust=False).mean()

def find_macd(data,span_long = 26,span_short = 12):
    ShortEMA = data.Close.ewm(span=span_short, adjust=False).mean()
    LongEMA = data.Close.ewm(span=span_long, adjust=False).mean()
    MACD = ShortEMA - LongEMA
    signal = MACD.ewm(span=9, adjust=False).mean()
    return signal

def find_rsi(data, span=14):
    ## span_Day RSI
    data['Up Move'] = np.nan
    data['Down Move'] = np.nan
    data['Average Up'] = np.nan
    data['Average Down'] = np.nan
    # Relative Strength
    data['RS'] = np.nan
    # Relative Strength Index
    data['RSI'] = np.nan
    ## Calculate Up Move & Down Move
    for x in range(1, len(data)):
        data['Up Move'][x] = 0
        data['Down Move'][x] = 0

        if data['Adj Close'][x] > data['Adj Close'][x - 1]:
            data['Up Move'][x] = data['Adj Close'][x] - data['Adj Close'][x - 1]

        if data['Adj Close'][x] < data['Adj Close'][x - 1]:
            data['Down Move'][x] = abs(data['Adj Close'][x] - data['Adj Close'][x - 1])

    ## Calculate initial Average Up & Down, RS and RSI
    data['Average Up'][span] = data['Up Move'][1:(span + 1)].mean()
    data['Average Down'][span] = data['Down Move'][1:(span + 1)].mean()
    data['RS'][span] = data['Average Up'][span] / data['Average Down'][span]
    data['RSI'][span] = 100 - (100 / (1 + data['RS'][span]))
    ## Calculate rest of Average Up, Average Down, RS, RSI
    for x in range((span + 1), len(data)):
        data['Average Up'][x] = (data['Average Up'][x - 1] * (span - 1) + data['Up Move'][x]) / span
        data['Average Down'][x] = (data['Average Down'][x - 1] * (span - 1) + data['Down Move'][x]) / span
        data['RS'][x] = data['Average Up'][x] / data['Average Down'][x]
        data['RSI'][x] = 100 - (100 / (1 + data['RS'][x]))
    return data





def find_entry_exit(df):
    ## Calculate the buy & sell signals
    ## Initialize the columns that we need
    df['Long Tomorrow'] = np.nan
    df['Buy Signal'] = np.nan
    df['Sell Signal'] = np.nan
    df['Buy RSI'] = np.nan
    df['Sell RSI'] = np.nan
    df['Strategy'] = np.nan
    ## Calculate the buy & sell signals
    for x in range(15, len(df)):
        # Calculate "Long Tomorrow" column
        if ((df['RSI'][x] <= 40) & (df['RSI'][x - 1] > 40)):
            df['Long Tomorrow'][x] = True
        elif ((df['Long Tomorrow'][x - 1] == True) & (df['RSI'][x] <= 70)):
            df['Long Tomorrow'][x] = True
        else:
            df['Long Tomorrow'][x] = False
        # Calculate "Buy Signal" column
        if ((df['Long Tomorrow'][x] == True) & (df['Long Tomorrow'][x - 1] == False)):
            df['Buy Signal'][x] = df['Adj Close'][x]
            df['Buy RSI'][x] = df['RSI'][x]
        # Calculate "Sell Signal" column
        if ((df['Long Tomorrow'][x] == False) & (df['Long Tomorrow'][x - 1] == True)):
            df['Sell Signal'][x] = df['Adj Close'][x]
            df['Sell RSI'][x] = df['RSI'][x]
    ## Calculate strategy performance
    df['Strategy'][15] = df['Adj Close'][15]
    for x in range(16, len(df)):
        if df['Long Tomorrow'][x - 1] == True:
            df['Strategy'][x] = df['Strategy'][x - 1] * (df['Adj Close'][x] / df['Adj Close'][x - 1])
        else:
            df['Strategy'][x] = df['Strategy'][x - 1]
    return df

def find_cpr(data):
    data['Pivot'] = (data['High'] + data['Low'] + data['Close']) / 3
    data['R1'] = 2 * data['Pivot'] - data['Low']
    data['S1'] = 2 * data['Pivot'] - data['High']
    data['R2'] = data['Pivot'] + (data['High'] - data['Low'])
    data['S2'] = data['Pivot'] - (data['High'] - data['Low'])
    data['R3'] = data['Pivot'] + 2 * (data['High'] - data['Low'])
    data['S3'] = data['Pivot'] - 2 * (data['High'] - data['Low'])
    next_day = data.tail(1).reset_index()[['Pivot', 'R1', 'R2', 'R3', 'S1', 'S2', 'S3']].to_dict()
    data[['Pivot', 'R1', 'R2', 'R3', 'S1', 'S2', 'S3']] = data[['Pivot', 'R1', 'R2', 'R3', 'S1', 'S2', 'S3']].shift(1)
    return next_day, data

