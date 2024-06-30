import pandas as pd
import os
import requests
from bottle import Bottle, response, request as bottle_request
from src.IO.utils import datatype_identifier
from src.engine.nainaio import NainaInput, NainaOutput


class TelegramIO(Bottle):
    BOT_URL = 'https://api.telegram.org/bot1043633896:AAGTiCkJ_J_v9tNkDTBHGbkNCuGr12I9FUE/'
    message_url = BOT_URL + 'sendMessage'

    def __init__(self, data):
        self.data = data
        self.type_data = datatype_identifier(data)
        self.username = ""

    def run_reply(self):
        self.param_extractor()
        self.pass_to_engine()
        self.send_reply_to_user()

    def pass_to_engine(self):
        self.reply_from_engine = "reply from engine"

    def param_extractor(self):
        self.chat_id = self.data['message']['chat']['id']
        self.message_text = self.data['message']['text']
        self.sender_name = self.data['message']['from']['first_name']

    def send_reply_to_user(self,data):
        # answer = "Hello " + self.sender_name + "\n\n\n From NAINA"
        json_data = {
            "chat_id": self.chat_id,
            "text": data,
        }
        return requests.post(self.message_url, json=json_data)

    def user_identification(self):
        df = pd.read_csv(os.getcwd()+"/src/data/userdata.csv")
        if self.chat_id in df.T_ID:
            self.username = df.loc[df.T_ID == self.chat_id , 'Username']
            return "success"
        else:
            data = "Please reply as below\n Note my Name : Your Name \n to let me know you better :)"
            self.send_reply_to_user(data)
            return "sent for registration"

