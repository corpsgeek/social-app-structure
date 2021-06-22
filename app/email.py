from flask_mail import Message
from app import mail
from flask import render_template
import os


def send_email(to, subject, template, **kwargs):
    msg = Message(os.environ.get('FLASK_MAIL_SUBJECT_PREFIX') + subject, sender=os.environ.get('FLASK_MAIL_SENDER'), recipients=[to])
    msg.body = render_template(template+'.txt', **kwargs)
    msg.html = render_template(template+'.html', **kwargs)
    mail.send(msg)
