# from bottle import run, post, request as bottle_request  # <--- we add bottle request
# from src.IO.telegram import TelegramIO

# @post('/telegram/')
# def main():  
#     content = bottle_request.json  # <--- extract all request data
#     print ("content",content)
#     telegram_obj = TelegramIO(content)
#     telegram_obj.run_reply()
    
# @post('/')
# def main():  
#     return "Hello Wortld"

# @post('/song_add')
# def song_add():
#     #username
#     #song url
#     #start time
#     #end time
#     #langauge
#     #genre
#     #type
#     #name_song
#     return "sucess"

# if __name__ == '__main__':  
#     run(host='0.0.0.0', port=3000, debug=True)






from flask import Flask, request
from bottle import Bottle, response, request as bottle_request

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


# @app.route('/telegram', methods=['POST'])
# def telegram():
#     # print (bottle_request.json)
#     content = request.get_json(force=True)
#     print ("content",content)
#     telegram_obj = TelegramIO(content)
#     telegram_obj.run_reply()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
#app.run(debug=True, host='0.0.0.0', port=8443, ssl_context=("/path/to/fullchain.pem", "/path/to/privkey.pem"))

# from flask import Flask
# from flask_restful import reqparse, abort, Api, Resource

# app = Flask(__name__)
# api = Api(app)



# from bot_telegram.bot_class import TelegramBot



# api.add_resource(TelegramBot, '/telegram')


# if __name__ == '__main__':
#     app.run(debug=True)
