import telebot
import json
from telebot import types
from db import loadDB, user_check, create_bid, check_bid, get_slots, delete_application, get_my_slot_category, get_my_slot_sex2, get_application_id, make_like, send_code, get_code, get_matcher_id
TOKEN = ""

bot = telebot.TeleBot(TOKEN) 


@bot.message_handler(commands=['start', 'help'])
def sex(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=3)
    itembtn1 = types.KeyboardButton('Парень')
    itembtn2 = types.KeyboardButton('Девушка')
    markup.add(itembtn1, itembtn2)
    bot.send_message(chat_id, "Отлично! Укажите, пожалуйста, свой пол: ", reply_markup=markup)

@bot.message_handler(regexp='Девушка')
def main_menu(message):
    global sex 
    sex = "Девушка"
    markup2 = types.ReplyKeyboardMarkup(row_width=3)
    itembtn1 = types.KeyboardButton('Оставить заявку')
    markup2.add(itembtn1)
    loadDB()
    msg = bot.send_message(message.chat.id, "Начнем?", reply_markup=markup2)

@bot.message_handler(regexp='Парень')
def main_menu(message):
    global sex 
    sex = "Парень"
    markup2 = types.ReplyKeyboardMarkup(row_width=3)
    itembtn1 = types.KeyboardButton('Оставить заявку')
    markup2.add(itembtn1)
    loadDB()
    msg = bot.send_message(message.chat.id, "Начнем?", reply_markup=markup2)

@bot.message_handler(regexp='Проверить статус заявки')
def check_status(message):
    if (check_bid(int(message.from_user.id))):
        code = get_code(int(message.from_user.id))
        bot.send_message(message.chat.id, 'На вашу заявку откликнулись! Код подтверждения встречи: {}'.format(code))
    else:
        bot.send_message(message.chat.id, "К сожалению, на вашу заявку никто не откликнулся")

@bot.message_handler(regexp='Оставить заявку')
def make_bid(message):
    markup3 = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Покурим')
    itembtn2 = types.KeyboardButton('Сходим в спортзал')
    itembtn3 = types.KeyboardButton('Выпьем кофе')
    itembtn4 = types.KeyboardButton('Пообедаем')
    itembtn5 = types.KeyboardButton('Прогуляемся')
    itembtn6 = types.KeyboardButton('Поучимся')
    markup3.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)
    msg = bot.send_message(message.chat.id, "Выбери категорию. Maybe We …", reply_markup=markup3)
    bot.register_next_step_handler(msg, save_category)

def save_category(message):
    global category
    category = message.text
    markup4 = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('Парень')
    itembtn2 = types.KeyboardButton('Девушка')
    itembtn3 = types.KeyboardButton('Без разницы')
    markup4.add(itembtn1, itembtn2, itembtn3)
    msg = bot.send_message(message.chat.id, "C кем ты хочешь провести время?", reply_markup=markup4)
    bot.register_next_step_handler(msg, save_sex2)

def save_sex2(message):
    global sex2
    sex2 = message.text
    markup = types.ReplyKeyboardRemove(selective=True)
    msg = bot.send_message(message.chat.id, "Когда ты хочешь встретиться? Желательно, распиши точную дату и время", reply_markup=markup)
    bot.register_next_step_handler(msg, save_bid)


def save_bid(message):
    global date_time
    date_time = message.text
    create_bid(int(message.from_user.id), category, sex, sex2, date_time)
    markup5 = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('Посмотреть другие заявки по запросу')
    itembtn2 = types.KeyboardButton('Проверить статус заявки')
    itembtn3 = types.KeyboardButton('Сбросить')
    markup5.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, "Ваша заявка сохранена", reply_markup=markup5)
    
@bot.message_handler(regexp="Посмотреть другие заявки по запросу")
def show_slots(message):
    category = get_my_slot_category(int(message.from_user.id))
    sex2 = get_my_slot_sex2(int(message.from_user.id))
    slots = get_slots(int(message.from_user.id), str(category), str(sex), str(get_my_slot_sex2))
    # print(slots)
    if slots == []:
        bot.send_message(message.chat.id, "К сожалению, по вашему запросу заявок нет")
    else:
        markup6 = types.ReplyKeyboardMarkup(row_width=1)
        for x in slots:
            itembtn = types.KeyboardButton('Заявка #{0}, Когда: {1}'.format(get_application_id(x[1]), x[4]))
            markup6.add(itembtn)
        itembtn8 = types.KeyboardButton('Назад')
        markup6.add(itembtn8)
        msg = bot.send_message(message.chat.id, "Заявки по вашему запросу:", reply_markup=markup6)
        bot.register_next_step_handler(msg, like)

@bot.message_handler(regexp='[Заявка #]\d+[, Когда: ].+')
def like(message):
    print(message.text)
    msg = str(message.text)
    first = msg.split(',')[0]
    app_id = int(first.split('#')[1])
    print(app_id)
    make_like(int(message.from_user.id), app_id)
    markup7 = types.ReplyKeyboardMarkup(row_width=1)
    itembtn = types.KeyboardButton('Отправить код подтверждения встречи вашему партнеру')
    markup7.add(itembtn)
    msg = bot.send_message(message.chat.id, "Вы поставили лайк!", reply_markup=markup7)

@bot.message_handler(regexp='Назад')
def nazad(message):
    markup5 = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('Посмотреть другие заявки по запросу')
    itembtn2 = types.KeyboardButton('Проверить статус заявки')
    itembtn3 = types.KeyboardButton('Сбросить')
    markup5.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, "Ваша заявка сохранена", reply_markup=markup5)    

@bot.message_handler(regexp='Сбросить')
def clear(message):
    delete_application(int(message.from_user.id))
    markup9 = types.ReplyKeyboardMarkup(row_width=1)
    itembtn3 = types.KeyboardButton('Оставить заявку')
    markup9.add(itembtn3)
    msg = bot.send_message(message.chat.id, "Ваша заявка удалена", reply_markup=markup9)
    

@bot.message_handler(regexp='Отправить код подтверждения встречи вашему партнеру')
def сode_sending(message):
    send_code(int(message.from_user.id))
    msg = bot.send_message(message.chat.id, "Введите код подтверждения")

@bot.message_handler(regexp='^\d{4}$')
def code_check(message):
    if message.text == str(get_code(message.from_user.id)):
        
        markup9 = types.ReplyKeyboardMarkup(row_width=1)
        itembtn3 = types.KeyboardButton('Вернуться в главное меню')
        markup9.add(itembtn3)
        msg = bot.send_message(message.chat.id, "Спасибо, встреча подтверждена", reply_markup=markup9)
    else:
        bot.send_message(message.chat.id, "Код подтверждения указан не верно. Введите еще раз")

    




bot.polling()