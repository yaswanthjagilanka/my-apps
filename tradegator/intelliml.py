from prophet import Prophet
import yfinance as yf
import numpy as np
import pandas as pd


def ensemble_prediction():
    pass


def run_prophet(data, predict_period=40):
    data = data.reset_index()
    print("data columns",data.columns)
    data = data[["Date", "Adj Close"]]
    data.columns = ["ds", "y"]
    m = Prophet()
    m.fit(data)
    future = m.make_future_dataframe(periods=predict_period)
    future.tail()
    forecast = m.predict(future)
    # forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
    forecast = forecast[['ds', 'trend','yhat', 'yhat_lower', 'yhat_upper']]
    return forecast,m


# def run_holtswinter(data=data, predict_period=predict_period):
#     pass
#
#
# def run_arima(data=data, predict_period=predict_period):
#     pass
