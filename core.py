#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import requests
import datetime
import config


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
        self.handlers = {}

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update


def polling():
    greet_bot = BotHandler(config.token)
    start_date = datetime.date(2018, 9, 3)
    new_offset = None

    while True:
        data = greet_bot.get_updates(new_offset)
        print(data)
        if data:
            last_update_id = data[0]['update_id']
            last_chat_text = data[0]['message']['text']
            last_chat_id = data[0]['message']['chat']['id']

            if last_chat_text.strip().lower() == '/week':
                now_date = datetime.datetime.now().date()
                print(now_date - start_date)
                week_num = (now_date - start_date).days // 7 + 1

                if week_num % 2 == 0:
                    parity = 'Знаменатель'
                else:
                    parity = 'Числитель'

                text = f'Сейчас {week_num} неделя ({parity})'
                greet_bot.send_message(last_chat_id, text)

            if last_chat_text.strip().lower() == '/add':
                pass

            new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        polling()
    except KeyboardInterrupt:
        exit()
