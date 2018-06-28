from flask_mail import Message
from app import mail, current_app
from flask import render_template
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)  # it needs to access attribute of the current app


def send_email(subject, sender, recipients, text_body, html_body,
               attachments=None, sync=False):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    if sync:
        mail.send(msg)
    else:
        # can handle other logic effectively at the same time
        Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


def send_password_reset_mail(user):
    token = user.get_reset_password_token()
    send_email('[Microblog] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token))
