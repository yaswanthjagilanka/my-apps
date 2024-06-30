import requests
from bottle import Bottle, response, request as bottle_request


class BotHandlerMixin:
    BOT_URL = None

    def __init__(self):
        pass

    def get_chat_id(self, data):
        """
        Method to extract chat id from telegram request.
        """
        chat_id = data['message']['chat']['id']
        return chat_id

    def get_message(self, data):
        """
        Method to extract message id from telegram request.
        """
        message_text = data['message']['text']
        return message_text

    def get_sender(self, data):
        """
        Method to extract message id from telegram request.
        """
        sender_name = data['message']['from']['first_name']
        return sender_name

    def send_message(self, prepared_data):
        """
        Prepared data should be json which includes at least `chat_id` and `text`
        """
        message_url = self.BOT_URL + 'sendMessage'
        return requests.post(message_url, json=prepared_data)


class TelegramBot(BotHandlerMixin, Bottle):
    BOT_URL = 'https://api.telegram.org/bot1043633896:AAGTiCkJ_J_v9tNkDTBHGbkNCuGr12I9FUE/'

    def __init__(self, *args, **kwargs):
        super(TelegramBot, self).__init__()
        self.route('/', callback=self.post_handler, method="POST")

    def change_text_message(self, text):
        return text[::-1]

    def prepare_data_for_answer(self, data):
        message = self.get_message(data)
        sender_name = self.get_sender(data)
        answer = self.change_text_message(message)
        chat_id = self.get_chat_id(data)
        answer = "Hello " + sender_name + "\n\n\n From NAINA"
        json_data = {
            "chat_id": chat_id,
            "text": answer,
        }
        return json_data

    def post_handler(self):
        data = bottle_request.json
        answer_data = self.prepare_data_for_answer(data)
        response = self.send_message(answer_data)
        return response


if __name__ == '__main__':
    app = TelegramBot()
    app.run(host='0.0.0.0', port=8080)