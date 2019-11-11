from pymongo import MongoClient
from credentials import bd as host
from random import randint
from botemail import verify_mail
from parsers import location_to_delta, list_to_datetime
from botcalendar import create_event
client = MongoClient(host, 27017)
db = client.test_bot_database
users = db.users
"""user = { 'chat_id' : 247893408,
        'e-mail' : 'denis.davydov8@open.ru',
        'works' : True,
        'incoming_events' : []
}"""


def add_user(chat_id, email):
    users = db.users
    OTP = randint(1000, 9999)
    user = {   'chat_id' : chat_id,
            'email' : email,
            'name': False,
            'surname': False,
            'works' : False,
            'OTP' : OTP,
            'incoming_events' : []    }
    mdb_uid = users.insert_one(user).inserted_id
    verify_mail(email, OTP)

def update_user(chat_id, updation):
    users = db.users
    user = users.find_one({'chat_id' : chat_id})
    if user:
        up = users.find_one_and_update(
        {'chat_id' : chat_id},
        {'$set' : {updation[0] : updation[1]}})

def check_user_OTP(chat_id, OTP):
    users = db.users
    user = users.find_one({'chat_id' : chat_id})
    print(int(user['OTP']) == int(OTP))
    if int(user['OTP']) == int(OTP):
        u = users.find_one_and_update({'chat_id' : chat_id}, {'$set': {'works' : True}})
        print(u)
        return True
    else:
        return False


def check_user(chat_id):
    users = db.users
    user = users.find_one({'chat_id' : chat_id})
    if user:
        return user['works']
    else:
        print('new user')
        return False

def add_event_request(chat_id):
    event_requests = db.event_requests
    print('start requesting')
    event_request = {    "init_chat_id" : chat_id,
    "location" : "location_name",
    "date" : "date",
    "time" : "time",
    "other_chat_id" : 0,
    "finished" : 0    }
    nid = event_requests.insert_one(event_request).inserted_id
    return nid

def update_event_request(chat_id, updation):
    event_requests = db.event_requests
#    print(chat_id, updation)
    if event_requests.find_one({'init_chat_id' : chat_id, "finished" : 0}):
        up = event_requests.find_one_and_update(
        {'init_chat_id' : chat_id, "finished" : 0}, #what we find
        {'$set' : {updation[0] : updation[1]}})
#        print(up)
        return up

def find_a_match(event_request):
    event_requests = db.event_requests
    print('fam er:', event_request)
    my_id = event_request['init_chat_id']
    location = event_request['location']
    date = event_request['date']
    time = event_request['time']
    print(location, date, time)
    match = db.event_requests.find_one_and_update(
    {"init_chat_id" : { "$ne" : my_id}, "other_chat_id" : 0, "location" : str(location), "date" : str(date), "time" : str(time), 'finished': 1},
#    {"other_chat_id" : 0, "location" : str(location), "date" : str(date), "time" : str(time), 'finished': 1},
    {"$set" : {"other_chat_id" : my_id}})
    if match:
        db.event_requests.find_one_and_update(
        {"init_chat_id" : my_id, "other_chat_id" : 0, "location" : str(location), "date" : str(date), "time" : str(time), 'finished': 1},
        {"$set" : {"other_chat_id" : match['init_chat_id']}})
        print('match -', match)
        my_co = users.find_one({'chat_id' : match['init_chat_id']})
        me = users.find_one({'chat_id' : event_request['init_chat_id']})
        print(my_co)
        delta = location_to_delta(location)
        start_end = list_to_datetime((date, time), delta)
        create_event(start_end, (my_co['name'], me['name']), location, (my_co['email'], me['email']))
        return (match, my_co, me)
    else:
        return False

def my_waiting_requests(chat_id):
    event_requests = db.event_requests
    my_er = event_requests.find({'init_chat_id' : chat_id, "other_chat_id" : 0})
    er_list = list()
    for er in my_er:
        er_list.append(er)
    return er_list

def my_matched_requests(chat_id):
    event_requests = db.event_requests
    my_er = event_requests.find({'init_chat_id' : chat_id, "other_chat_id" : 1})
    er_list = list()
    for er in my_er:
        er_list.append(er)
    return er_list
