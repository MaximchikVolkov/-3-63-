# -*- coding: utf-8 -*-
import telebot
import requests
import json

access_key = "c879e061-51a9-403f-9d04-45fd24ecc72e"
telegram_token = '6828596676:AAE4M7tHHrZr40oWkyn9sr3sM3KZGG6vk4Y'

headers = {
    "X-Yandex-API-Key": access_key
}

query_now = """{
  weatherByPoint(request: { lat: 55.452, lon: 37.373 }) {
    now {
      temperature
    }
  }
}"""

query_forecast = """{
  weatherByPoint(request: { lat: 55.452, lon: 37.373 }) {
    forecast {
      days(limit: 1) {
        time
        parts {
          morning {
            avgTemperature
          }
          day {
            avgTemperature
          }
          evening {
            avgTemperature
          }
          night {
            avgTemperature
          }
        }
      }
    }
  }
}"""

tele_bot = telebot.TeleBot(telegram_token)

@tele_bot.message_handler(commands=['start'])
def start(msg):
    user_name = msg.from_user.first_name
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Температура сейчас']])
    keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Прогноз погоды']])
    tele_bot.send_message(msg.chat.id, 'Привет, ' + user_name + '! \nЯ - бот, показывающий погоду! Могу предложить следующее:'
                            , reply_markup=keyboard)

@tele_bot.callback_query_handler(func=lambda msg: msg.data)
def result(msg):
    if msg.data == 'Температура сейчас':
        response = requests.post('https://api.weather.yandex.ru/graphql/query', headers=headers, json={'query': query_now})
        todos = json.loads(response.text)
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Температура сейчас']])
        keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Прогноз погоды']])
        tele_bot.send_message(msg.message.chat.id, 'Сейчас в Москве ' + str(todos['data']['weatherByPoint']['now']['temperature']) + ' градусов',
                              reply_markup=keyboard)
        

    elif msg.data == 'Прогноз погоды':
        response = requests.post('https://api.weather.yandex.ru/graphql/query', headers=headers, json={'query': query_forecast})
        todos = json.loads(response.text)
        morning_temp = str(todos['data']['weatherByPoint']['forecast']['days'][0]['parts']['morning']['avgTemperature'])
        day_temp = str(todos['data']['weatherByPoint']['forecast']['days'][0]['parts']['day']['avgTemperature'])
        evening_temp = str(todos['data']['weatherByPoint']['forecast']['days'][0]['parts']['evening']['avgTemperature'])
        night_temp = str(todos['data']['weatherByPoint']['forecast']['days'][0]['parts']['night']['avgTemperature'])
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Температура сейчас']])
        keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Прогноз погоды']])
        tele_bot.send_message(msg.message.chat.id, 'Завтра в Москве будет следующая погода: \n' +
                              'Утром - ' + morning_temp + ' градусов\n' + 
                              'Днём - ' + day_temp + ' градусов\n' +
                              'Вечером - ' + evening_temp + ' градусов\n' +
                              'Ночью - ' + night_temp + ' градусов',
                              reply_markup=keyboard)
        

# @tele_bot.message_handler(content_types=['text'])
# def text_handler(msg):
#     # text = msg.text
#     # url = 'https://api.vk.com/method/wall.post'
#     # data = {'close_comments': 1, 'friends_only': 1, 'access_token': vk_token, 'owner_id': user_id, 'message': text, 'v': 5.199}
#     # r = requests.post(url, params=data)
#     # if (r.status_code == 200):
#     #     tele_bot.send_message(msg.chat.id, 'Успешный успех!')
#     # else:
#     #     tele_bot.send_message(msg.chat.id, 'Произошли какие-то неполадки(')
    

tele_bot.polling(none_stop=True)