# -*- coding: utf-8 -*-
import telebot

class TelegramBot(telebot.TeleBot):
    count_men = 0
    count_women = 0
    count_cat = 0
    count_dogs = 0
    count_plane = 0
    count_veg = 0

token = "6828596676:AAE4M7tHHrZr40oWkyn9sr3sM3KZGG6vk4Y"
bot = TelegramBot(token)

@bot.message_handler(commands=['start'])
def start(msg):
    user_name = msg.from_user.first_name
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Мальчики', 'Девочки']])
    keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Кошечки', 'Собачки']])
    keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Вертолёт', 'Баклажан']])
    bot.send_message(msg.chat.id, 'Привет, ' + user_name + '! Давай решим кого в МГТУ им. Н.Э. Баумана больше! '
                                '\n\nВыбирай', reply_markup=keyboard)

def keyboard(msg):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Мальчики', 'Девочки']])
    keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Кошечки', 'Собачки']])
    keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Вертолёт', 'Баклажан']])
    bot.send_message(msg.message.chat.id, 'Выбирай:', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda msg: msg.data)
def result(msg):
    if msg.data == 'Мальчики':
        bot.count_men += 1
        bot.send_message(msg.message.chat.id, 'За Мальчиков проголосовали ' + str(bot.count_men) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За Девочек проголосовали ' + str(bot.count_women) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За Кошечек проголосовали ' + str(bot.count_cat) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За Собачек проголосовали ' + str(bot.count_dogs) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За ???Вертолётов??? проголосовали ' + str(bot.count_plane) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За ???Баклажанов??? проголосовали ' + str(bot.count_veg) + ' раз(-а)')
        keyboard(msg)
    elif msg.data == 'Девочки':
        bot.count_women += 1
        bot.send_message(msg.message.chat.id, 'За Мальчиков проголосовали ' + str(bot.count_men) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За Девочек проголосовали ' + str(bot.count_women) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За Кошечек проголосовали ' + str(bot.count_cat) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За Собачек проголосовали ' + str(bot.count_dogs) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За ???Вертолётов??? проголосовали ' + str(bot.count_plane) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За ???Баклажанов??? проголосовали ' + str(bot.count_veg) + ' раз(-а)')
        keyboard(msg)
    elif msg.data == 'Кошечки':
        bot.count_cat += 1
        bot.send_message(msg.message.chat.id, 'За Мальчиков проголосовали ' + str(bot.count_men) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За Девочек проголосовали ' + str(bot.count_women) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За Кошечек проголосовали ' + str(bot.count_cat) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За Собачек проголосовали ' + str(bot.count_dogs) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За ???Вертолётов??? проголосовали ' + str(bot.count_plane) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За ???Баклажанов??? проголосовали ' + str(bot.count_veg) + ' раз(-а)')
        keyboard(msg)
    elif msg.data == 'Собачки':
        bot.count_dogs += 1
        bot.send_message(msg.message.chat.id, 'За Мальчиков проголосовали ' + str(bot.count_men) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За Девочек проголосовали ' + str(bot.count_women) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За Кошечек проголосовали ' + str(bot.count_cat) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За Собачек проголосовали ' + str(bot.count_dogs) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За ???Вертолётов??? проголосовали ' + str(bot.count_plane) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За ???Баклажанов??? проголосовали ' + str(bot.count_veg) + ' раз(-а)')
        keyboard(msg)
    elif msg.data == 'Вертолёт':
        bot.count_plane += 1
        bot.send_message(msg.message.chat.id, 'За Мальчиков проголосовали ' + str(bot.count_men) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За Девочек проголосовали ' + str(bot.count_women) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За Кошечек проголосовали ' + str(bot.count_cat) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За Собачек проголосовали ' + str(bot.count_dogs) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За ???Вертолётов??? проголосовали ' + str(bot.count_plane) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За ???Баклажанов??? проголосовали ' + str(bot.count_veg) + ' раз(-а)')
        keyboard(msg)
    elif msg.data == 'Баклажан':
        bot.count_veg += 1
        bot.send_message(msg.message.chat.id, 'За Мальчиков проголосовали ' + str(bot.count_men) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За Девочек проголосовали ' + str(bot.count_women) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За Кошечек проголосовали ' + str(bot.count_cat) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За Собачек проголосовали ' + str(bot.count_dogs) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За ???Вертолётов??? проголосовали ' + str(bot.count_plane) + ' раз(-а)')
        bot.send_message(msg.message.chat.id, 'За ???Баклажанов??? проголосовали ' + str(bot.count_veg) + ' раз(-а)')
        keyboard(msg)

bot.polling(none_stop=True)