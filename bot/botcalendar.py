from ics import Calendar, Event
from botemail import send_invitaion
from datetime import datetime as dt
c = Calendar()
e = Event()
def create_event(start_end, names, location, mails):
    e.name = "Выпить кофе"
    e.begin = start_end[0]
    e.end = start_end[1]
    e.description = f'{names[0]} и {names[1]} пьют кофе и знакомятся в городе {location}'
    c.events.add(e)
    print(e)
    filename = start_end[0].strftime("%Y%m%dT%H%M%S%f")# + '.ics'
    print(list(mails))
    print(filename)
    print(c)
    with open(f'{filename}.ics', 'w') as my_file:
        print('open file')
        my_file.writelines(c)
    print('try to e-mail')
    send_invitaion(mails, f'{filename}.ics')#here we call function to return our event via mail. althoug it is possible to send via chat 
