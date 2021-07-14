import telebot
from telebot import types
import os

token = "1788567444:AAFbRBpRTR7iUdf4qN7X94MnHg0-BI1X8ZI"
bot = telebot.TeleBot(token)

print(bot.get_me())

@bot.message_handler(commands = ["start"])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True,False)
    user_markup.row("/start")
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton("Заказать пиццу")
    item2 = types.KeyboardButton("Корзина")

    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Добро пожаловать в пиццерию \U0001F600", reply_markup=markup)

@bot.message_handler(content_types = ["text"])
def handle_text(message):
    if message.text == "Заказать пиццу":
        markup = types.InlineKeyboardMarkup(row_width=3)
        item1 = types.InlineKeyboardButton("Пепперони", callback_data = "button1")
        item2 = types.InlineKeyboardButton("Маргарита",callback_data = "button2" )
        item3 = types.InlineKeyboardButton("Гавайская", callback_data="button3")

        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, 'Какую пиццу вы предпочитаете?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'button1':
                directory = 'F:/пицца'
                all_files_in_directory = os.listdir(directory)
                print (all_files_in_directory)
                img = open(directory + '/' + 'Без названия (2).jfif', 'rb' )
                bot.send_chat_action(call.message.chat.id, 'upload_photo')
                bot.send_photo(call.message.chat.id, img, 'Пеперони — острая разновидность салями итало-американского происхождения, а также название пиццы '
                                                       'американского происхождения. Делается из свинины, хотя встречаются американские разновидности, приготовленные из курицы, говядины и т.д')
                img.close()



                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("30 см", callback_data="button4")
                item2 = types.InlineKeyboardButton("40 см", callback_data="button5")

                markup.add(item1, item2)
                bot.send_message(call.message.chat.id, 'Выберите размер:',reply_markup=markup)


            elif call.data == "button2":
                directory = 'F:/пицца'
                all_files_in_directory = os.listdir(directory)
                img = open(directory + '/' + 'маргарита.jpg', 'rb')
                bot.send_chat_action(call.message.chat.id, 'upload_photo')
                bot.send_photo(call.message.chat.id, img , "Пицца «Маргарита» - это традиционное итальянское блюде, известное во всем мире. Ее состав максимально простой, но вкус никого не оставляет равнодушным.")
                img.close()

                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("30 см", callback_data="button6")
                item2 = types.InlineKeyboardButton("40 см", callback_data="button7")

                markup.add(item1, item2)
                bot.send_message(call.message.chat.id, 'Выберите размер:', reply_markup=markup)

            elif call.data == "button3":
                directory = 'F:/пицца'
                all_files_in_directory = os.listdir(directory)
                img = open(directory + '/' + 'hawaiian-pizza_09.jpg', 'rb')
                bot.send_chat_action(call.message.chat.id, 'upload_photo')
                bot.send_photo(call.message.chat.id, img , "Гавайская пицца — пицца, приготовляемая с использованием томатного соуса, сыра, ананасов и ветчины.")
                img.close()

                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("30 см", callback_data="button8")
                item2 = types.InlineKeyboardButton("40 см", callback_data="button9")

                markup.add(item1, item2)
                bot.send_message(call.message.chat.id, 'Выберите размер:', reply_markup=markup)

            elif call.data == 'button4':
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Пепперони 30 см добавлена в корзину!\U0001F600")

            elif call.data == 'button5':
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Пепперони 40 см добавлена в корзину!\U0001F600")

            elif call.data == 'button6':
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Маргарита 30 см добавлена в корзину!\U0001F600")

            elif call.data == 'button7':
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Маргарита 40 см добавлена в корзину!\U0001F600")

            elif call.data == 'button8':
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Гавайская пицца 30 см добавлена в корзину!\U0001F600")

            elif call.data == 'button9':
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Гавайская пицца 40 см добавлена в корзину!\U0001F600")

    except Exception as e:
        print(repr(e))


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text == "Корзина":
        bot.send_message(message.chat.id, '')
    else:
        bot.send_message(message.chat.id, 'Корзина пуста')


bot.polling(none_stop=True, interval=0)