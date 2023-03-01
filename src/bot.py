import config as cf
import telebot
from telebot import types
from telebot.types import InlineKeyboardButton

from main import *

# token = '5679216888:AAEnHl7wKQmR4mXwrqWQQIVGVztbqtINeBQ'
bot = telebot.TeleBot(cf.token)

# @bot.message_handler(commands=['start'])
# def start_message(message):
#     bot.send_message(message.chat.id,'Привет')

my_direct = Direct()

@bot.message_handler(commands=['start'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item2 = types.KeyboardButton("Выбрать институт")
    markup.add(item2)

    # path = first_start()        #это запустит селениум и скачает файл это очень долго, надо что-то другое
    my_direct.set_path('/Users/katherine.marakhova/PycharmProjects/exampleBot/files/3-курс-бакалавриат-ОФО-50.xlsx')    #передаем нашему объекту путь к обработанному файлу

    bot.send_message(message.chat.id,'Привет! \nЯ бот-хранитель твоего распиания! \nДля начала, нужно выбрать институт', reply_markup = markup)

@bot.message_handler(content_types='text')
def message_reply(message):

    if message.text == "Выбрать институт":
        markup = types.InlineKeyboardMarkup()

        my_direct.get_list_inst()

        for name in my_direct.list_insts:
            btn = types.InlineKeyboardButton(text = str(name), callback_data = str(name))
            markup.add(btn)
        bot.send_message(message.chat.id, "Бакалавриат. Институты ГУУ:", reply_markup = markup)


@bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
    req = call.data.split('_')
    # список листов full_inst_list
    if req[0] in my_direct.list_insts:  # получили название института

        markup = types.InlineKeyboardMarkup()

        my_direct.set_inst(req[0])      # добавили в наш объект выбранный институт
        my_direct.get_dict_napr()       # формируем лист направлений

        for name in my_direct.list_napr:
            if name == 'None':continue

            if len(name) > 32:          # колбек не поддерживает текст больше 32 символов, поэтому его нужно обрезать
                btn = types.InlineKeyboardButton(text = name, callback_data = name[:33])
                markup.add(btn)
                continue
            btn = types.InlineKeyboardButton(text=name, callback_data=name)
            markup.add(btn)
        m = "Направления " + req[0] + ":"
        bot.send_message(call.message.chat.id, m, reply_markup=markup)

    if req[0] in my_direct.list_napr:
        bot.send_message(call.message.chat.id, "Отлично! Теперь нужно выбрать группу")
        my_direct.set_path(req[0])


    if req[0] == 'unseen':
        bot.delete_message(call.message.chat.id, call.message.message_id)

bot.infinity_polling()
