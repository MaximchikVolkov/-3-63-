# -*- coding: utf-8 -*-
import requests
import telebot
import xml.dom.minidom
from datetime import date  
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

token = '6828596676:AAE4M7tHHrZr40oWkyn9sr3sM3KZGG6vk4Y'

class TelegramBot(telebot.TeleBot):
    select_date = ''

bot = TelegramBot(token)

@bot.message_handler(commands=['start'])
def start(msg):
    bot.select_date = ''
    user_name = msg.from_user.first_name
    bot.send_message(msg.chat.id, 'Привет, ' + user_name + '! Я могу показать курс валюты к рублю в выбранный день.')
    calendar, step = DetailedTelegramCalendar(max_date=date.today()).build()
    bot.send_message(msg.chat.id, f"Выбери дату:  {LSTEP[step]}", reply_markup=calendar)

@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar(max_date=date.today()).process(c.data)
    if not result and key:
        bot.edit_message_text(f"Выбери дату: {LSTEP[step]}",
        c.message.chat.id,
        c.message.message_id,
        reply_markup=key)
    elif result:
        send_valute_keyboard(c)
        bot.edit_message_text(f"Была выбрана следующая дата: {result}",
        c.message.chat.id,
        c.message.message_id)
        bot.select_date = str(result.strftime('%d-%m-%Y'))

@bot.callback_query_handler(func=lambda c: c.data)
def get_text_valute(c):
    if c.data == 'Азербайджанский манат':
        get_value(c.message.chat.id, 'R01020A', 'Курс Азербайджанского маната - ')
    elif c.data == 'Белорусский рубль':
        get_value(c.message.chat.id, 'R01090B', 'Курс Белорусского рубля - ')
    elif c.data == 'Польский злотый':
        get_value(c.message.chat.id, 'R01565', 'Курс Польского злотого - ')
    elif c.data == 'Казахстанский тенге':
        get_value(c.message.chat.id, 'R01335', 'Курс Казахстанского тенге - ')
    elif c.data == 'Поменять дату':
        calendar, step = DetailedTelegramCalendar(max_date=date.today()).build()
        bot.send_message(c.message.chat.id, f"Выбери дату:  {LSTEP[step]}", reply_markup=calendar)

def send_valute_keyboard(msg):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Азербайджанский манат', 'Белорусский рубль']])
    keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Польский злотый', 'Казахстанский тенге']])
    keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Поменять дату']])
    bot.send_message(msg.message.chat.id, 'Выбери валюту:', reply_markup=keyboard)

def get_value(id, valute_id, name):
    
    url = 'https://www.cbr.ru/scripts/XML_daily.asp?date_req=' + bot.select_date
    
    r = requests.get(url)
    dom = xml.dom.minidom.parseString(r.text)
    dom.normalize()

    nodes = dom.getElementsByTagName("ValCurs")
    value = nodes[0].childNodes[0].nodeValue

    nodes = dom.getElementsByTagName("Valute")

    for i in range(nodes.length):
        if nodes[i].getAttribute("ID") == valute_id:
            index = i
            break
    
    value = nodes[index].getElementsByTagName("Value")[0].childNodes[0].nodeValue
    bot.send_message(id, name + value)

bot.polling(none_stop=True)