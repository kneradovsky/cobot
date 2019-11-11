from telegram import replykeyboardmarkup, replykeyboardremove
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters

from credentials import TBToken, bd

from keyboards import reg_keyboard, reg_keyboard2, loc_keyboard, locations, date_keyboard, dates, time_keyboard, times
from parsers import email_validator, otp_validator, name_surname_validator, name_surname_extractor
from DBMS import add_user, check_user, update_user, check_user_OTP, add_event_request, update_event_request, find_a_match, my_matched_requests, my_waiting_requests

updater = Updater(token=TBToken)
JQ = updater.job_queue
dispatcher = updater.dispatcher

reg_markup = replykeyboardmarkup.ReplyKeyboardMarkup(reg_keyboard, one_time_keyboard=True)
reg_markup2 = replykeyboardmarkup.ReplyKeyboardMarkup(reg_keyboard2, one_time_keyboard=True)
loc_markup = replykeyboardmarkup.ReplyKeyboardMarkup(loc_keyboard, one_time_keyboard=True)
date_markup = replykeyboardmarkup.ReplyKeyboardMarkup(date_keyboard, one_time_keyboard=True)
time_markup = replykeyboardmarkup.ReplyKeyboardMarkup(time_keyboard, one_time_keyboard=True)


def start(bot, update, args):
    print("start started")
    c_i = update.message.chat_id
    c_u = check_user(c_i)
    if c_u:
        bot.send_message(chat_id=c_i, text="Хочешь выпить чашечку кофе?", reply_markup=reg_markup)
    else:
        bot.send_message(chat_id=c_i, text="Напиши свою рабочую почту. Это нужно, чтобы я мог прислать тебе код, потому что-то коллеги из ДИБ просили меня не разговаривать с незнакомцами.")

def echo(bot, update):
    c_i = update.message.chat_id
    print('got echo c_i: ', c_i)
    text = update.message.text
    print("{}".format(text))
#    """    o_v = otp_validator(text)
#    c_u = check_user(c_i)
#    e_v = email_validator(text)
#    n_s = name_surname_validator(text)[0]
#    print(f'otp_validator(text) - {o_v}')
#    print(f'check_user(c_i) - {c_u}')
#    print(f'email_validator(text) - {e_v}')
#    print(f'name_surname_validator(text)[0] - {n_s}')
    if email_validator(text):
        add_user(c_i, text)
        bot.send_message(chat_id=c_i, text="Прекрасно, спасибо! С минуты на минуту тебе придёт письмо с четырёхзначным паролем. Пришли мне его, чтобы я знал, что ты - это ты.")
        #        bot.send_message(chat_id=c_i, text="Прекрасно, спасибо! Можешь теперь ещё добавить свои имя и фамилию, использую команды /name и /surname соответственно? После того, как наберёшь команду, сразу пиши имя или фамилию. Например: '/name Петя' - позволит представиться Петей, а /nameМаша - нет.")
    elif check_user(c_i) == False and otp_validator(text) == True:
        r = check_user_OTP(c_i, text)
        if r:
            bot.send_message(chat_id=c_i, text="Ура, я теперь я вижу, что тебе можно доверять! \nДумаю, теперь самое время познакомиться. Пожалуйста, напиши 'Меня зовут Имя Фамилия' и после этого можно будет выпить чашечку кофе >^_^<")
    elif check_user(c_i) == False and email_validator(text) == False and otp_validator(text) == False:
        bot.send_message(chat_id=c_i, text="Странно, но вы не похожи на сотрудника банка :(")
    elif name_surname_validator(text):
        print('name validated')
        n_s = name_surname_extractor(text)
        updation = ("name", n_s[0])
        update_user(c_i, updation=updation)
        updation = ("surname", n_s[1])
        update_user(c_i, updation=updation)
        bot.send_message(chat_id=c_i, text="Всё, с формальностями закончили, теперь можно и кофе выпить. Ты же хочешь кофе?\nPS Если захочешь поменять имя и фамилию, то просто ещё раз напиши 'Меня зовут Имя Фамилия'", reply_markup=reg_markup)
    elif text in locations:
        updation = ("location", text)
        u_e = update_event_request(chat_id=c_i, updation=updation)
        bot.send_message(chat_id=c_i, text="А когда?", reply_markup=date_markup)
    elif text in dates:
        updation = ("date", text)
        u_e = update_event_request(chat_id=c_i, updation=updation)
        bot.send_message(chat_id=c_i, text="Во сколько?", reply_markup=time_markup)
    elif text in times:
        updation = ("time", text)
        u_e = update_event_request(chat_id=c_i, updation=updation)
        updation = ("finished", 1)
        up = update_event_request(chat_id=c_i, updation=updation)
        bot.send_message(chat_id=c_i, text="Я создал заявку. Когда подберу кого-нибудь, дам знать.", reply_markup=reg_markup2)
        print(up)
        print('try to find')
        fi = find_a_match(up)
        try:
            match = fi[0]
            bot.send_message(chat_id=c_i, text="Уже нашёл! Ищи приглашение в почте :)", reply_markup=reg_markup2)
            bot.send_message(chat_id=c_i, text="Локация: {0} \nДата и время: {1} {2} \nСотрудник: {3} {4}\nE-mail {5}".format(match['location'], match['date'], match['time'], fi[1]['name'], fi[1]['email']))
            bot.send_message(chat_id=fi[1]['chat_id'], text="На ваше приглашение откликнулись!\nЛокация: {0} \nДата и время: {1} {2}\nСотрудник: {3} {4} \nE-mail {5}".format(match['location'], match['date'], match['time'], fi[2]['name'], fi[2]['surname'], fi[2]['email']))
        except BaseException as be:
            print(type(be), be)
    elif text in  ['Да, хочу!', 'Хочу ещё кофе!']:
        print("try to add e_r")
        i = add_event_request(c_i)
        print(i)
        bot.send_message(chat_id=c_i, text="Где будет кофе-брейк?", reply_markup=loc_markup)
        print('message sent')
    elif text == 'Мои подтверждённые заявки':
        mmr = my_matched_requests(chat_id=c_i)
        print(mmr)
    elif text == 'Мои неподтверждённые заявки':
        mwr = my_waiting_requests(chat_id=c_i)
        print(mwr)
    else:
        bot.send_message(chat_id=c_i, text="Я тебя не понимаю :(")
    print('end of echo')

def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text = "Я бы помог, но у меня лапки :(")

def name(bot, update, args):
    text = " ".join(args)
    updation = ("name", text)
    if text:
        update_user(chat_id=update.message.chat_id, updation=updation)
        bot.send_message(chat_id=update.message.chat_id, text = "Спасибо! Теперь фамилию, использую команду /surname")

def surname(bot, update, args):
    text = " ".join(args)
    updation = ("surname", text)
    if text:
        update_user(chat_id=update.message.chat_id, updation=updation)
        bot.send_message(chat_id=update.message.chat_id, text = "Спасибо!\nТеперь может быть хочешь кофе?", reply_markup=reg_markup)


start_handler = CommandHandler('start', start, pass_args=True)
name_handler = CommandHandler('name', name, pass_args=True)
surname_handler = CommandHandler('surname', surname, pass_args=True)

echo_handler = MessageHandler(Filters.text, echo)

help_handler = CommandHandler('help', help)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(name_handler)
dispatcher.add_handler(surname_handler)


#job_clock = JQ.run_repeating(clock, interval = 60*60*1, first = datetime.datetime(datetime.datetime.today().year,datetime.datetime.today().month,datetime.datetime.today().day, 11, 15))

updater.start_polling()
