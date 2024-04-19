# -*- coding: utf-8 -*-
import telebot
import requests

user_id = 279586664
telegram_token = '6828596676:AAE4M7tHHrZr40oWkyn9sr3sM3KZGG6vk4Y'
vk_token = 'vk1.a.zlxqGwoUMLqyfkn8xYENgvz9WcBUV7O40bLtWxTm9C7mfWWIFTyDxhSg_j0IHf4FWnfmr-MdmjTaprpniH-1QXq0_HKVx4mvEhVMTx8yLEy_rdxhwxbFLHYLMTE5N9St5pK7Prv0AejoOm0WMNbwnodwIdEVYMkMJ6HHxMIetFEypCRylRriipGdT1rrr8R0lx5gQf67uI8cOYeU9CnrAA'

tele_bot = telebot.TeleBot(telegram_token)

@tele_bot.message_handler(commands=['start'])
def start(msg):
    tele_bot.send_message(msg.chat.id, 'Привет! Я - бот, который преобразует твои сообщения в посты ВКонтакте. Скорее напиши мне что-нибудь!')

@tele_bot.message_handler(content_types=['text'])
def text_handler(msg):
    text = msg.text
    url = 'https://api.vk.com/method/wall.post'
    data = {'close_comments': 1, 'friends_only': 1, 'access_token': vk_token, 'owner_id': user_id, 'message': text, 'v': 5.199}
    r = requests.post(url, params=data)
    if (r.status_code == 200):
        tele_bot.send_message(msg.chat.id, 'Успешный успех!')
    else:
        tele_bot.send_message(msg.chat.id, 'Произошли какие-то неполадки(')

tele_bot.polling(none_stop=True)