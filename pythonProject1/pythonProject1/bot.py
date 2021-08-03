import telebot
from telebot import types
import os
import sqlite3
import sqlite3 as lite
import sys

token = "1788567444:AAFbRBpRTR7iUdf4qN7X94MnHg0-BI1X8ZI"
bot = telebot.TeleBot(token)

con = lite.connect('dbpizza.db')
with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM Пиццы")
    rows = cur.fetchall()

def insert_varible_into_table(user_id, title, size, kolvo):
    try:
        sqlite_connection = sqlite3.connect('dbpizza.db')
        global cursor
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_insert_with_param = """INSERT INTO Пиццы
                              (user_id, title, size, kolvo)
                              VALUES (?, ?, ?, ?);"""

        data_tuple = (user_id, title, size, kolvo)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)


menu1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
item1 = types.KeyboardButton("Заказать пиццу \U0001f355")
item2 = types.KeyboardButton("Корзина \U0001f5d1")
menu1.add(item1, item2)

menu2 = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True)
item1 = types.KeyboardButton("Пепперони \U0001f355")
item2 = types.KeyboardButton("Маргарита \U0001f355")
item3 = types.KeyboardButton("Гавайская \U0001f355")
menu2.add(item1, item2, item3)

sizepep = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
item1 = types.KeyboardButton("30 см")
item2 = types.KeyboardButton("40 см")
sizepep.add(item1, item2)

vbor = types.InlineKeyboardMarkup(row_width=2)
item1 = types.InlineKeyboardButton("Да! \U0001f60d", callback_data="da")
item2 = types.InlineKeyboardButton("Назад \U0001f519", callback_data="nazad")
vbor.add(item1, item2)

yesno = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
item1 = types.KeyboardButton("Да! \U0001f60d")
item2 = types.KeyboardButton("Нет \u274e")
yesno.add(item1, item2)

glmem = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
item1 = types.KeyboardButton("В Главное меню \U0001f519")
glmem.add(item1)

START, TITLE, SIZE, KOLVO, CONFIRMATION = range(5)
from collections import defaultdict
user_state = defaultdict(lambda : START)
def get_state(message):
    return user_state[message.chat.id]
def update_state(message, state):
    user_state[message.chat.id] = state

CORZINA = defaultdict(lambda : { })
def update_corzina(user_id, key, value):
    CORZINA[user_id][key] = value
def get_corzina(user_id):
    return CORZINA[user_id]
def del_corzina(user_id):
    del CORZINA[user_id]

@bot.message_handler(commands = ["start"])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row("/start")
    bot.send_message(message.chat.id, "Добро пожаловать в пиццерию \U0001F600", reply_markup=menu1)
    global us_id
    us_id = message.chat.id

@bot.message_handler(func=lambda message:get_state(message) == START)
def handle_text(message):
    if message.text == "Заказать пиццу \U0001f355":
        bot.send_message(message.chat.id, 'Какую пиццу вы предпочитаете?', reply_markup=menu2)

    elif message.text == 'Корзина \U0001f5d1':
        bot.send_message(message.chat.id, text='В корзине: {}'.format(rows))

    elif message.text == 'Пепперони \U0001f355':
         directory = 'images'
         all_files_in_directory = os.listdir(directory)
         print(all_files_in_directory)
         img = open(directory + '/' + 'Без названия (2).jfif', 'rb' )
         bot.send_photo(message.chat.id, img, 'Пеперони — острая разновидность салями итало-американского происхождения, а также название пиццы '
                                              'американского происхождения. Делается из свинины, хотя встречаются американские разновидности, приготовленные из курицы, говядины и т.д')
         img.close()
         bot.send_message(message.chat.id, 'Выбрать пиццу: \n' + message.text + '?', reply_markup=vbor)

    elif message.text == 'Маргарита \U0001f355':
         directory = 'images'
         img = open(directory + '/' + 'маргарита.jpg', 'rb')
         bot.send_photo(message.chat.id, img , "Пицца «Маргарита» - это традиционное итальянское блюде, известное во всем мире. Ее состав максимально простой, но вкус никого не оставляет равнодушным.")
         img.close()
         bot.send_message(message.chat.id, 'Выбрать пиццу: \n' + message.text + '?', reply_markup=vbor)

    elif message.text == "Гавайская \U0001f355":
         directory = 'images'
         img = open(directory + '/' + 'hawaiian-pizza_09.jpg', 'rb')
         bot.send_photo(message.chat.id, img , "Гавайская images — images, приготовляемая с использованием томатного соуса, сыра, ананасов и ветчины.")
         img.close()
         bot.send_message(message.chat.id, 'Выбрать пиццу: ' + '\n' + message.text + '?', reply_markup=vbor)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.data:
            if call.data == 'da':
                update_state(call.message, TITLE)
                update_corzina(call.message.chat.id, 'Название', call.message.text[16:-1])
                global title_us
                title_us=call.message.text[16:-1]
                bot.send_message(call.message.chat.id, 'Выберите размер:', reply_markup=sizepep)
                update_state(call.message, SIZE)

            elif call.data == 'nazad':
                bot.send_message(call.message.chat.id, "Вы вернулись к выбору пицц \U0001f914", reply_markup=menu2)

    except Exception as e:
        print(repr(e))

@bot.message_handler(func=lambda message: get_state(message) == SIZE)
def handle_size(message):
    update_corzina(message.chat.id, 'Размер:', message.text)
    global size_us
    size_us = message.text
    bot.send_message(message.chat.id, text='Укажите количество в шт:')
    update_state(message, KOLVO)

@bot.message_handler(func=lambda message: get_state(message) == KOLVO)
def handle_kolvo(message):
    update_corzina(message.chat.id, 'Количество:', message.text)
    global kolvo_us
    kolvo_us = message.text
    global corzina
    corzina = get_corzina(message.chat.id)
    bot.send_message(message.chat.id, text='Добавить в корзину? {}'.format(corzina) , reply_markup=yesno)
    update_state(message, CONFIRMATION)

@bot.message_handler(func=lambda message: get_state(message) == CONFIRMATION)
def handle_confirmation(message):
    if message.text == "Да! \U0001f60d":
        bot.send_message(message.chat.id , text= 'Добавлено в корзину!' , reply_markup=glmem)
        insert_varible_into_table(user_id=us_id, title=title_us, size=size_us, kolvo=kolvo_us)
        update_state(message, START)

    elif message.text == "Нет \u274e":
        bot.send_message(message.chat.id, "Вы вернулись в Главное меню!", reply_markup=menu1)
        update_state(message, START)

    elif message.text == 'В Главное меню \U0001f519':
        bot.send_message(message.chat.id,"Вы вернулись в Главное меню!", reply_markup=menu1)
        update_state(message, START)

bot.polling(none_stop=True, interval=0)