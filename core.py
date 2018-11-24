#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import requests
import datetime
import config
from SQLighter import SQLighter


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
        self.handlers = {}
        self.questions = ['Введите тип события', 'Введите текст напоминаня',
                          'Введите дату и время \nВ формате MM-DD-YYYY HH:MM']

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        print("RESP.JSON ", resp.json())
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def dialog(self):
        for q in self.questions:
            yield q


def polling():
    bot = BotHandler(config.token)
    start_date = datetime.date(2018, 9, 3)
    new_offset = None

    while True:
        data = bot.get_updates(new_offset)
        print("DATA", data)
        if data:
            last_update_id = data[0]['update_id']
            last_chat_text = data[0]['message']['text']
            chat_id = data[0]['message']['chat']['id']

            if bot.handlers.get(chat_id, None):

                if bot.handlers[chat_id]['current_q'] == bot.questions[2]:
                    try:
                        datetime.datetime.strptime(last_chat_text.strip(), '%d-%m-%Y %H:%M')
                        bot.handlers[chat_id]['error'] = False
                    except ValueError:
                        bot.send_message(chat_id, 'Неверный формат \nПовторите ввод ')
                        bot.handlers[chat_id]['error'] = True

                if not bot.handlers[chat_id]['error']:
                    bot.handlers[chat_id]['answers'].append(last_chat_text.strip())
                    try:
                        text = next(bot.handlers[chat_id]['dialog'])
                        bot.handlers[chat_id]['current_q'] = text
                        bot.send_message(chat_id, text)
                    except StopIteration:
                        # Make record in DB
                        with SQLighter(config.db_name) as db_worker:
                            db_worker.save(bot.handlers[chat_id]['answers'])

                        bot.send_message(chat_id, 'Событие добавлено')
                        # Reset handlers
                        bot.handlers[chat_id] = None

            if last_chat_text.strip().lower() == '/week':
                now_date = datetime.datetime.now().date()
                print(now_date - start_date)
                week_num = (now_date - start_date).days // 7 + 1

                if week_num % 2 == 0:
                    parity = 'Знаменатель'
                else:
                    parity = 'Числитель'

                text = f'Сейчас {week_num} неделя ({parity})'
                bot.send_message(chat_id, text)

            if last_chat_text.strip().lower() == '/add':
                # Init dialog
                bot.handlers[chat_id] = {'dialog': bot.dialog(),
                                         'answers': [],
                                         'current_q': '',
                                         'error': False}

                text = next(bot.handlers[chat_id]['dialog'])
                bot.handlers[chat_id]['current_q'] = text
                bot.send_message(chat_id, text)

            if last_chat_text.strip().lower() == '/list':
                pass

            new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        polling()
    except KeyboardInterrupt:
        exit()
