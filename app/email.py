from flask_mail import Message
from flask import render_template

def send_email(app, mail, subject, sender, recipients, text_body, html_body):
    with app.app_context():  # Ensure app context is active when sending emails
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = text_body
        msg.html = html_body
        mail.send(msg)

def send_password_reset_email(app, mail, user):
    token = user.get_reset_password_token()
    send_email(app, mail,
               '[Microblog] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token))
