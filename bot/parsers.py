import re
from datetime import datetime, timedelta, time

def keyboard_to_list(keyboard):
    l = list()
    for key in keyboard:
        l.append(key[0])
    return l

def location_to_delta(location):#maybe it's better to use UTC timezones, but for start there is simple timedelta according to location
    delta = 0
    if 'Москва' in location:
        pass
    elif 'Казань' in location:
        pass
    elif 'Саратов' in location:
        delta = 1
    elif 'Екатеринбург' in location:
        delta = 2
    elif 'Ханты-Мансийск' in location:
        delta = 2
    elif 'Новосибирск' in location:
        delta = 4
    elif 'Хабаровск' in location:
        delta = 7
    return delta

def list_to_datetime(str_list, delta): #simple translation from human-readable to machine-readable format of datetime objects
    today = datetime.now()
    days_delta = timedelta(days=0)
    start_hour = 9
    predate = str_list[0]
    pretime = str_list[1]
    if predate == 'Сегодня':
        pass
    elif predate == 'Завтра':
        days_delta = timedelta(days=1)
    else:
        days_delta = timedelta(days=2)
    if pretime == 'C 9 до 10':
        pass
    else:
        start_hour = int(pretime[2:4])
    start_hour += delta
    almost_datetime = today + days_delta
    start = datetime.combine(almost_datetime.date(), time(start_hour, 0, 0))
    end = start + timedelta(hours=1)
    return (start, end)

#I guess the following is obvious
def email_validator(text):
    m = re.search(".+@open.ru", text)
    if m:
        return True
    else:
        return False

def otp_validator(text):
    m = re.search("[0-9]{4}", text)
    if m:
        return True
    else:
        return False

def name_surname_validator(text):
    print('start name validation')
    command = str(text).lower()[0:11]#magic range of 'command' "Меня зовут"
    print(command)
    if command == 'Меня зовут '.lower():
        return True#(true, name_surname)
    else:
        return False

def name_surname_extractor(text):
    text_s = text.split()
    name_surname = (text_s[2], text_s[3])
    return name_surname
