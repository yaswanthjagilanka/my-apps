from flask import Flask, request,render_template
from src.audio_puller import audio_dwnld
from flask_ngrok import run_with_ngrok
import json
# from flask import Flask
# from bottle import Bottle, response, request as bottle_request
# import json
# import ast

app = Flask(__name__)
# CORS(app)
dict_out= {}

from pyngrok import ngrok
ngrok.set_auth_token("25oByfqScAQZah27b59Ka9774ks_3TFDyByz6PwdiyGB3AzfQ")


@app.route('/hello')
def hello():
    return "hello"


@app.route('/')
def audio_collect():
    return render_template('base1.html')

@app.route('/audio_recv',methods = ['POST', 'GET'])
def audio_recv():
    result = request.form
    print (result['language'])
    for key in result.keys():
        print (key)


    with open('database.json') as json_file:
        dict_out = json.load(json_file)
    for x in dict_out.values():
        if result['url'] == x['URL']:
            return render_template('exists.html')
    else:
        filename = audio_dwnld.audio_process(result)
        if len(dict_out.keys())>0:
            id1 = int(max(dict_out.keys()))+1
        else:
            id1 = int(0)
        print("id1:",id1)
        dict_out[int(id1)] = { "Name" : filename, "User": result['username'],"Language" : result['language'], "Genre" : result['genre'] , "URL" : result['url']}
        print("dict",dict_out)
        with open('database.json', 'w') as outfile:
            json.dump(dict_out, outfile)

        return render_template('return_page.html')

@app.route('/song_add')
def song_add():
    #username
    #song url
    #start time
    #end time
    #langauge
    #genre
    #type
    #name_song
    return "sucess"

# run_with_ngrok(app)
if __name__ == '__main__':
    app.debug = True
    # app.run()
    app.run(host='localhost', port=8080)