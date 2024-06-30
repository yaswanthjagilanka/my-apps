from tracemalloc import start
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
from datetime import datetime
from flask import Flask, render_template
import pandas as pd
import json
import time
import warnings

from query_processing import query_and_matching

warnings.filterwarnings("ignore")

global classvar

@app.route('/')
def index():
    global start
    start  = time.time()
    return render_template('index.html')

@app.route('/query_input', methods=['POST'])
def query_input():
    if request.method == 'POST':
        projectpath = request.form['category']
        print(projectpath)
        global classvar
        classvar=projectpath
        return render_template('query_input.html')
    else:
        return render_template('query_response.html')

@app.route('/query_response', methods=['POST','GET'])
def query_response():
    if request.method == 'POST':
        if classvar=="CS":
            path = "OutputFiles_ComputerScience/"
        else:
            path = "OutputFiles_ComputerVision/"
        path = "data/"+path
        query = request.form['search']
        outdf, outjson = query_and_matching(path,query)
        global endtime
        endtime = time.time()
        print("Seconds since epoch =", endtime-start)
        return render_template('out.html',  tables=[outdf.to_html(classes='data')], titles=outdf.columns.values)
    else:
    # your code
    # return a response
        return render_template('out.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)