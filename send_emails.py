from flask.ext.mail import Message
from threading import Thread
from flask import render_template
from app import db, mail, app, models

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

def send_actual_async_email(app, msg):
    with app.app_context():
        with mail.connect() as conn:
            conn.send(msg)

def send_email(subject, sender, recipients, text_body, html_body, reply_to = 'aristaec1617@gmail.com'):
    msg = Message(subject, sender = sender, recipients = [recipients], reply_to = reply_to, bcc=['ec@stuyarista.org'])
    msg.body = text_body
    msg.html = html_body
    send_actual_async_email(app, msg)

def send_test_email():
    with app.app_context():
        with mail.connect() as conn:
            for user in models.User.query.all():
                msg = Message('Open House -- Important Information', 
                              sender = app.config['MAIL_DEFAULT_SENDER'], 
                              recipients = [user.email], reply_to = 'aristaec1617@gmail.com', bcc=['ec@stuyarista.org'])
                msg.body = 'HTML Error'
                msg.html = render_template('email_to_students.html', fname = user.fname)
                conn.send(msg)
