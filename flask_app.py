
# A very simple Flask Hello World app for you to get started with...

import telebot
import conf     # импортируем наш секретный токен
import random
#import time
import pandas as pd
import flask
from flask import Flask

app = Flask(__name__)
WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)
bot = telebot.TeleBot(conf.TOKEN, threaded=False)  # создаем экземпляр бота

bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)


#data.head()



alluserids = set()

# этот обработчик запускает функцию send_welcome, когда пользователь отправляет команды /start или /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    alluserids.add(message.chat.id)
    bot.send_message(message.chat.id, "\n\t".join(["Здравствуйте! Это бот-нейросеть, который каждый день генерирует восточную притчу!", "Бот принимает следующие команды:", " /any - случайная басня", "/arm - армянская басня", "/hasid - хасидская басня", "/ind - индийская басня", "/jew - еврейская басня", "/suf - суфийская басня"]))


@bot.message_handler(commands=['any']) # здесь описываем, на какие сообщения реагирует функция
def anybasnya(message):

    alltexts = open(r"/home/NeuroBasnya/mysite/all.txt", "r").readlines()
    reply = str(random.choice(alltexts))
    alluserids.add(message.chat.id)
    bot.send_message(message.chat.id, reply)



@bot.message_handler(commands=['ind']) # здесь описываем, на какие сообщения реагирует функция
def indbasnya(message):

    X = open(r"/home/NeuroBasnya/mysite/ind.txt", "r").readlines()
    reply = str(random.choice(X))
    alluserids.add(message.chat.id)
    bot.send_message(message.chat.id, reply)

@bot.message_handler(commands=['arm']) # здесь описываем, на какие сообщения реагирует функция
def armbasnya(message):
    X = open(r"/home/NeuroBasnya/mysite/arm.txt", "r").readlines()
    reply = str(random.choice(X))
    alluserids.add(message.chat.id)
    bot.send_message(message.chat.id, reply)

@bot.message_handler(commands=['hasid']) # здесь описываем, на какие сообщения реагирует функция
def hasidbasnya(message):
    X = open(r"/home/NeuroBasnya/mysite/hasid.txt", "r").readlines()
    reply = str(random.choice(X))
    alluserids.add(message.chat.id)
    bot.send_message(message.chat.id, reply)

@bot.message_handler(commands=['jew']) # здесь описываем, на какие сообщения реагирует функция
def jewbasnya(message):
    X = open(r"/home/NeuroBasnya/mysite/jew.txt", "r").readlines()
    reply = str(random.choice(X))
    alluserids.add(message.chat.id)
    bot.send_message(message.chat.id, reply)


@bot.message_handler(commands=['suf']) # здесь описываем, на какие сообщения реагирует функция
def sufbasnya(message):
    X = open(r"/home/NeuroBasnya/mysite/suf.txt", "r").readlines()
    reply = str(random.choice(X))
    alluserids.add(message.chat.id)
    bot.send_message(message.chat.id, reply)

@bot.message_handler(func=lambda m: True)  # этот обработчик реагирует все прочие сообщения
def other(message):
	bot.send_message(message.chat.id, 'Задайте боту команду, пожалуйста')


# пустая главная страничка для проверки
"""@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

if __name__ == '__main__':
    bot.polling(none_stop=True)
    while True:
        for elem in alluserids:
            global data
            i = random.choice(1,len(data))
            reply = data.title.iloc[i] +"\n" + data.text.iloc[i]
            bot.send_message(elem, reply)
            time.sleep(2)
        time.sleep(86400)"""

# обрабатываем вызовы вебхука = функция, которая запускается, когда к нам постучался телеграм
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else: flask.abort(403)