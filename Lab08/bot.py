# -*- coding: utf-8 -*-

import telebot

class Counter():
    def __init__(self):
        self.black_humor = 0
        self.white_humor = 0
        self.joke_1 = 0
        self.joke_2 = 0
        self.joke_3 = 0
        self.joke_4 = 0
    

token = "6828596676:AAE4M7tHHrZr40oWkyn9sr3sM3KZGG6vk4Y"

bot = telebot.TeleBot(token)
counter = Counter()

def start_lvl(msg):
    if msg.text == "Чёрный юмор":
        counter.black_humor += 1
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[telebot.types.KeyboardButton(name) for name in ['Машинист', 'Родственник', 'В начало']])
        bot.send_message(msg.chat.id, 'Ох, сейчас возня пойдет! Пойдет сейчас возня. Выбирай)'
                         '\n\nЦенитель черного юмора тыкнул сюда аж ' + str(counter.black_humor) + ' тыка', reply_markup=keyboard)
    else:
        counter.white_humor += 1
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[telebot.types.KeyboardButton(name) for name in ['Вовочка и публичный дом', 'Бобёр', 'В начало']])
        bot.send_message(msg.chat.id, 'Супер! Я тоже не люблю чёрных, так какой анекдот ты хочешь услышать, семпай?'
                         '\n\nПсс, ты кстати решил послушать НЕ черные шутки ' + str(counter.white_humor) +' раз', reply_markup=keyboard)


def black_jokes(msg):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[telebot.types.KeyboardButton(name) for name in ['Машинист', 'Родственник', 'В начало']])
    if msg.text == 'Машинист':
        counter.joke_1 += 1
        bot.send_message(msg.chat.id, 'Шёл однажды вдоль железной дороги и вдруг вижу — поезд сбивает черного парня. Моя первая мысль: "Чёрт, это же мог быть я!".'
                         '\nУстроился машинистом на следующий же день.'
                                    '\n\nТы послушал анекдот про Машиниста - ' + str(counter.joke_1) + ' раз(а)', reply_markup=keyboard)
    elif msg.text == 'Родственник':
        counter.joke_2 += 1
        bot.send_message(msg.chat.id, 'У семьи каннибалов умер родственник. И грустно и вкусно.'
                                    '\n\nТы пополнил свой запас анекдотом про Родственника - ' + str(counter.joke_2) + ' раз(а)', reply_markup=keyboard)

def white_jokes(msg):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[telebot.types.KeyboardButton(name) for name in ['Вовочка и публичный дом', 'Бобёр', 'В начало']])
    if msg.text == 'Вовочка и публичный дом':
        counter.joke_3 += 1
        bot.send_message(msg.chat.id, 'Девочки из Вовочкиного класса договорились, что, если Вовочка скажет какую-нибудь пошлость, то они встанут и выйдут из класса. Начался урок, и учитель спрашивает:'
                         '\nДети, а что нового строится в нашем городе?'
                         '\n— Школа.'
                         '\n— Библиотека!'
                         '\n— Музей!'
                         '\nВовочка:'
                         '\n— Публичный дом.'
                         '\nДевочки встают и выходят из класса, а'
                         '\nВовочка им кричит:'
                         '\n— Куда же вы? Там же только фундамент залили!'
                                    '\n\nАнекдот про Вовочку и публичный дом был прочитан - ' + str(counter.joke_3) + ' раз(а)', reply_markup=keyboard)
    elif msg.text == 'Бобёр':
        counter.joke_4 += 1
        bot.send_message(msg.chat.id, 'К сожалению, этот легендарный анекдот может рассказывать только легендарный человек \n(Тассов Кирилл Леонидович)'
                                    '\n\nТы посмеялся (или нет) над этим - ' + str(counter.joke_4) + ' раз(а)', reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def start(msg):
    user_name = msg.from_user.first_name
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[telebot.types.KeyboardButton(name) for name in ['Чёрный юмор', 'НЕ чёрный юмор']])
    bot.send_message(msg.chat.id, 'Привет, ' + user_name + '! Я создан, чтобы рассказывать тебе анекдоты!!!'
                                '\nКакие анекдоты хочешь послушать?', reply_markup=keyboard)
    

@bot.message_handler(content_types=['text'])
def text(msg):
    if msg.text in ['Чёрный юмор', 'НЕ чёрный юмор']:
        start_lvl(msg)
    elif msg.text in ['Машинист', 'Родственник']:
        black_jokes(msg)
    elif msg.text in ['Вовочка и публичный дом', 'Бобёр']:
        white_jokes(msg)
    else:
        start(msg)

bot.polling(none_stop=True)