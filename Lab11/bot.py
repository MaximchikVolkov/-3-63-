# -*- coding: utf-8 -*-
import requests
import telebot
import xml.dom.minidom
from datetime import date  
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

token = '6828596676:AAE4M7tHHrZr40oWkyn9sr3sM3KZGG6vk4Y'

class TelegramBot(telebot.TeleBot):
    select_date_0 = ''
    select_date_1 = ''
    counter = 0

bot = TelegramBot(token)

@bot.message_handler(commands=['start'])
def start(msg):
    bot.select_date_0 = ''
    bot.select_date_1 = ''
    user_name = msg.from_user.first_name
    bot.send_message(msg.chat.id, 'Привет, ' + user_name + '! Я могу показать курс валюты к рублю за выбранный период.')
    calendar, step = DetailedTelegramCalendar(max_date=date.today()).build()
    
    bot.send_message(msg.chat.id, f"Выбери дату от:  {LSTEP[step]}", reply_markup=calendar)
    bot.send_message(msg.chat.id, f"Выбери дату до:  {LSTEP[step]}", reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar(max_date=date.today()).process(c.data)
    if not result and key:
        if 'до' in c.message.text:
            text = "Выбери дату до"
        else:
            text = "Выбери дату от"
        bot.edit_message_text(f"{text}: {LSTEP[step]}",
        c.message.chat.id,
        c.message.message_id,
        reply_markup=key)
    elif result:
        if 'до' in c.message.text:
            text = "Была выбрана следующая дата до:"
            bot.select_date_1 = str(result.strftime('%d-%m-%Y'))
        else:
            text = "Была выбрана следующая дата от:"
            bot.select_date_0 = str(result.strftime('%d-%m-%Y'))
        bot.edit_message_text(f"{text} {result}",
        c.message.chat.id,
        c.message.message_id)
        bot.counter+=1
        if bot.counter == 2:
            bot.counter = 0
            send_valute_keyboard(c)
        

@bot.callback_query_handler(func=lambda c: c.data)
def get_text_valute(c):
    if c.data == 'Азербайджанский манат':
        get_value(c, 'R01020A', 'Азербайджанский манат')
    elif c.data == 'Белорусский рубль':
        get_value(c, 'R01090B', 'Белорусский рубль')
    elif c.data == 'Польский злотый':
        get_value(c, 'R01565', 'Польский злотый')
    elif c.data == 'Казахстанский тенге':
        get_value(c, 'R01335', 'Казахстанский тенге')
    elif c.data == 'Поменять дату':
        calendar, step = DetailedTelegramCalendar(max_date=date.today()).build()
        bot.send_message(c.message.chat.id, f"Выбери дату от:  {LSTEP[step]}", reply_markup=calendar)
        bot.send_message(c.message.chat.id, f"Выбери дату до:  {LSTEP[step]}", reply_markup=calendar)

def send_valute_keyboard(msg):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Азербайджанский манат', 'Белорусский рубль']])
    keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Польский злотый', 'Казахстанский тенге']])
    keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Поменять дату']])
    bot.send_message(msg.message.chat.id, 'Выбери валюту:', reply_markup=keyboard)

def get_value(msg, valute_id, name):
    data = []
    date = []
    url = 'https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=' + bot.select_date_0 + '&date_req2=' + bot.select_date_1 + '&VAL_NM_RQ=' + valute_id
    
    r = requests.get(url)
    dom = xml.dom.minidom.parseString(r.text)
    dom.normalize()

    nodes = dom.getElementsByTagName("Record")
    
    for i in range(nodes.length):
        value = nodes[i].getElementsByTagName("Value")[0].childNodes[0].nodeValue
        day = nodes[i].getAttribute("Date")
        date.append(day)
        data.append(value)
    
    for i in range(0, len(data)):
        data[i] = float(data[i].replace(',', '.'))
    
    fig, ax = plt.subplots() 
    ax.plot(date, data, color="g")
    plt.xticks(rotation=45)
    plt.title(name)
    
    plt.savefig("graph.png", bbox_inches='tight')
    # plt.close()

    bot.send_photo(msg.message.chat.id, photo=open('graph.png', 'rb'))
    send_valute_keyboard(msg)

bot.polling(none_stop=True)