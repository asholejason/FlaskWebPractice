from flask_mail import Message
from threading import Thread
from app import mail
from .main import main


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(to, subject, template, **kwargs):
    msg = Message(main.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=main.config['FLASKY_MAIL_SENDER'],
                  recipients=[to])
    # msg.body = render_template(template + '.txt', **kwargs)
    # msg.html = render_template(template + '.html', **kwargs)
    msg.body = template
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
