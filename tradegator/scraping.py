import numpy as np
import pandas as pd

# Data Source
import yfinance as yf

# Data viz
import plotly.graph_objs as go





def scrape_data(start_period, end_period, interval,ticker_stock='AAPL'):
    if interval:
        return yf.download(tickers=ticker_stock, start=start_period, end=end_period,interval='1m')
    return yf.download(tickers=ticker_stock, start=start_period, end=end_period)
