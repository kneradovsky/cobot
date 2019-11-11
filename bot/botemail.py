import smtplib
from email.message import EmailMessage
from os import remove

from credentials import smtp_pass, smtp_user

def verify_mail(mail, code):
    smtpObj = smtplib.SMTP(host='smtp.mail.ru')
    smtpObj.starttls()
    smtpObj.login(user=smtp_user, password=smtp_pass)
    msg = form_reg_msg(code, smtp_user, mail)
    smtpObj.send_message(msg=msg)
    smtpObj.close()

def send_invitaion(mails, event):
    print('try to invite')
    smtpObj = smtplib.SMTP(host='smtp.mail.ru')
    smtpObj.starttls()
    smtpObj.login(user=smtp_user, password=smtp_pass)
    msg = form_invitation(smtp_user, mails, event)
    smtpObj.send_message(msg=msg)
    smtpObj.close()
    print('inveited')
    remove(f'{filename}.ics')
    print('cleaning done')

def form_reg_msg(code, sent_from, sent_to):
    content = '''Доброго времени суток, коллега!
Ваш адрес электронной почты был указан при регистрации в Кофеботе. Если это были Вы, то оправьте боту следующий код:
'''
    content += str(code)
    content += '''
Заранее спасибо и хорошего кофепития!
Искренне Ваш,
Кофе бот "Кофе Кот"
    '''
    print(content)
    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = 'Код авторизации для Кофебота'
    msg['From'] = sent_from
    msg['To'] = sent_to
    print(msg)
    return msg

def form_invitation(sent_from, sent_to):
    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = 'Приглашение от Кофебота'
    msg['From'] = sent_from
    msg['To'] = sent_to
    msg.attach(event, 'text/calendar')
    print(msg)
    return msg
