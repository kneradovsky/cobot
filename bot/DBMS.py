from pymongo import MongoClient
from datetime import datetime
from credentials import bd as host
client = MongoClient('84.201.173.78', 27017)
#client = MongoClient(host, 27017)
db = client.test_bot_database
users = db.users
"""user = { 'chat_id' : 247893408,
        'e-mail' : 'denis.davydov8@open.ru',
        'works' : True,
        'incoming_events' : []
}"""


def add_user(chat_id, email):
    users = db.users
    user = {   'chat_id' : chat_id,
            'email' : email,
            'name': 'John',
            'surname': 'Dow',
            'works' : True,
            'incoming_events' : []    }
    mdb_uid = users.insert_one(user).inserted_id
    print(mdb_uid)

def update_user(chat_id, updation):
    users = db.users
    user = users.find_one({'chat_id' : chat_id})
    if user:
        up = users.find_one_and_update(
        {'chat_id' : chat_id},
        {'$set' : {updation[0] : updation[1]}})
        print(up)


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
    location = event_request['location']
    date = event_request['date']
    time = event_request['time']
    print(location, date, time)
    match = db.event_requests.find_one({"other_chat_id" : 0, "location" : location, "date" : date, "time" : time, 'finished': 1})[0]
    print('match -', match)
    return match

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
