import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from os import remove

from credentials import smtp_pass, smtp_user, smtp_host

def verify_mail(mail, code):
    print('start verification')
    try:
        smtpObj = smtplib.SMTP(host=smtp_host)
        smtpObj.starttls()
        smtpObj.login(user=smtp_user, password=smtp_pass)
        msg = form_reg_msg(code, smtp_user, mail)
        smtpObj.send_message(msg=msg)
        smtpObj.close()
    except BaseException as be:
        print(be)

def send_invitaion(mails, event):
    print('try to invite')
    smtpObj = smtplib.SMTP(host=smtp_host)
    smtpObj.starttls()
    smtpObj.login(user=smtp_user, password=smtp_pass)
    try:
        msg = form_invitation(smtp_user, ', '.join(list(mails)), event)
        smtpObj.send_message(msg=msg)
        smtpObj.close()
    except BaseException as be:
        print(be)
    remove(event)

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
    return msg

def form_invitation(sent_from, sent_to, event):
    print('try to form invitation')
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Приглашение от Кофебота'
    msg['From'] = sent_from
    msg['To'] = sent_to
    part1 = MIMEMultipart('Приглашение во вложении.', 'plain')
    print('first')
    part2 = MIMEMultipart(event, 'text/calendar')
    print('second')
    msg.attach(part1)
    msg.attach(part2)
    print(msg)
#    with open (event) as fp
#        msg.set_content(fp.read())
#        msg.
#    msg.add_attachment(event, '/calendar')
    return msg
