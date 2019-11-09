#https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-–-Your-first-Bot
#https://groosha.gitbooks.io/telegram-bot-lessons/content/chapter8.html
__rev = 0.1
__upd = 0

import httplib2
import urllib
import json

from telegram import replykeyboardmarkup, replykeyboardremove
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters

#from SQL import init_tables, injector, roles
#from SQL import read_name, add_name, get_m_r_i, upd_m_r_i, add_member_role, get_role, is_role

from credentials import TBToken, bd
#from credentials import vk_access_token as token

from keyboards import reg_keyboard, reg_keyboard2, loc_keyboard, locations, date_keyboard, dates, time_keyboard, times
from parsers import email_validator
from DBMS import add_user, check_user, update_user, add_event_request, update_event_request, find_a_match, my_matched_requests, my_waiting_requests

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
        bot.send_message(chat_id=c_i, text="Напиши свою рабочую почту, чтобы я мог тебе писать холодными зимними вечерами.")

def echo(bot, update):
    c_i = update.message.chat_id
    print('got echo c_i: ', c_i)
    text = update.message.text
    print(f'{text}')
    if check_user(c_i) == False and email_validator(text) == False:
        bot.send_message(chat_id=c_i, text="Странно, но вы не похожи на сотрудника банка :(")
    if email_validator(text):
        add_user(c_i, text)
        bot.send_message(chat_id=c_i, text="Прекрасно, спасибо! Можешь теперь ещё добавить свои имя и фамилию, использую команды /name и /surname соответственно? После того, как наберёшь команду, сразу пиши имя или фамилию. Например: '/name Петя' - позволит представиться Петей, а /nameМаша - нет.")
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
            print(up['location'])
            print(len(fi))
            bot.send_message(chat_id=c_i, text="Уже нашёл! Смотри:", reply_markup=reg_markup2)
        except BaseException as BE:
            print(type(BE), BE)
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
        bot.send_message(chat_id=c_i, text=f"Я тебя не понимаю :(")
    print('end of echo')

def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text = f"""
    """)

def name(bot, update, args):
    text = " ".join(args)
    updation = ("name", text)
    if text:
        update_user(chat_id=update.message.chat_id, updation=updation)
        bot.send_message(chat_id=update.message.chat_id, text = f"""Спасибо!""")

def surname(bot, update, args):
    text = " ".join(args)
    updation = ("surname", text)
    if text:
        update_user(chat_id=update.message.chat_id, updation=updation)
        bot.send_message(chat_id=update.message.chat_id, text = f"""Спасибо!""")


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
