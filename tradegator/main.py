from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px
from PIL import Image
import base64
import io
import plotly.graph_objs as go

import warnings

warnings.filterwarnings("ignore")

from technicalanalysis import *
from scraping import *

from intelliml import *


@app.route('/handle_data', methods=['POST'])
def handle_data():
    tickerstock = request.form.get('sel1')
    hedge_ratio = int(request.form.get('hedge'))
    nonrisk = (100 - hedge_ratio) / 2
    risk = 100 - nonrisk
    amount = request.form.get('amount')
    print(tickerstock, hedge_ratio, amount)
    data = scrape_data(datetime.now() - relativedelta(years=10), datetime.now(), ticker_stock=tickerstock,
                       interval=False)
    # data1 = scrape_data(datetime.now() - relativedelta(days=7), datetime.now(), ticker_stock=tickerstock,interval='1m')
    if find_trend(data, days=10):
        print("True")
        macd = find_macd(data, span_long=26, span_short=12)
        rsi_data = find_rsi(data, span=14)
        entry_exit = find_entry_exit(data)
        cprpoints, cprdata = find_cpr(data)
        buy = entry_exit.tail(1)[['Buy Signal']]
        if np.isnan(buy.values[0][0]):  # is not nan:
            buy_signal = "No Buy Signal Right now"
        else:
            buy_signal = buy.values[0][0]
        sell = entry_exit.tail(1)[['Sell Signal']]
        if np.isnan(sell.values[0][0]):  # is not nan:
            sell_signal = "No Sell Signal Right now"
        else:
            sell_signal = sell.values[0][0]
    else:
        print("False")
        return render_template('hello.html')

    pivot_point = "{:.2f}".format(cprpoints['Pivot'][0])
    R1 = "{:.2f}".format(cprpoints['R1'][0])
    R2 = "{:.2f}".format(cprpoints['R2'][0])
    R3 = "{:.2f}".format(cprpoints['R3'][0])
    S1 = "{:.2f}".format(cprpoints['S1'][0])
    S2 = "{:.2f}".format(cprpoints['S2'][0])
    S3 = "{:.2f}".format(cprpoints['S3'][0])

    forecast, m = run_prophet(data=data, predict_period=60)
    fig1 = m.plot(forecast)
    import io
    my_stringIObytes = io.BytesIO()
    fig1.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read())

    data = yf.download(tickers=tickerstock, period='1d', interval='1m')

    # declare figure
    fig = go.Figure()

    # Candlestick
    trace1 = go.Candlestick(x=data.index,
                            open=data['Open'],
                            high=data['High'],
                            low=data['Low'],
                            close=data['Close'], name='market data')
    data1 = [trace1]
    graphJSON = json.dumps(data1, cls=plotly.utils.PlotlyJSONEncoder)

    # count = forecast.shape[0]
    # # xScale = np.linspace(0, 100, count)
    # # yScale = np.random.randn(count)
    # xScale = forecast.ds
    # yScale = forecast.trend
    # # Create a trace
    # trace = go.Scatter(
    #     x=xScale,
    #     y=yScale
    # )

    # data = [trace]
    # graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('notdash.html',
                           graphJSON=graphJSON, tickerstock=tickerstock, pivot=pivot_point, R1=R1,
                           R2=R2, R3=R3, S1=S1, S2=S2, S3=S3, img_data=my_base64_jpgData.decode('utf-8'),
                           sell_signal=sell_signal, hedge_ratio=hedge_ratio, risk=risk, nonrisk=nonrisk,
                           buy_signal=buy_signal)


@app.route('/index')
def index():
    # projectpath = request.form['projectFilepath']
    # your code
    # return a response
    return render_template('index.html')

@app.route('/')
def index1():
    # projectpath = request.form['projectFilepath']
    # your code
    # return a response
    return render_template('index.html')


@app.route('/home')
def home():
    # projectpath = request.form['projectFilepath']
    # your code
    # return a response
    return render_template('hello.html')


def get_candlestick(tickerstock):
    data = yf.download(tickers='tickerstock', period='2d', interval='1m')

    # declare figure
    fig = go.Figure()

    # Candlestick
    fig.add_trace(go.Candlestick(x=data.index,
                                 open=data['Open'],
                                 high=data['High'],
                                 low=data['Low'],
                                 close=data['Close'], name='market data'))

    # Add titles
    fig.update_layout(
        title='Uber live share price evolution',
        yaxis_title='Stock Price (USD per Shares)')

    # X-Axes
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=15, label="15m", step="minute", stepmode="backward"),
                dict(count=45, label="45m", step="minute", stepmode="backward"),
                dict(count=1, label="HTD", step="hour", stepmode="todate"),
                dict(count=3, label="3h", step="hour", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    # Show
    my1_stringIObytes = io.BytesIO()
    fig.savefig(my1_stringIObytes, format='jpg')
    my1_stringIObytes.seek(0)
    my1_base64_jpgData = base64.b64encode(my1_stringIObytes.read())
    return my1_base64_jpgData


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080, debug=True)
