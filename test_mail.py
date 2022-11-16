from flask import current_app
from flask_mail import Message
from app import mail

msg = Message(
    "Test", 
    recipients=['abdurrasheedfalaludaura@gmail.com'],
    sender=current_app.config['MAIL_USERNAME'],
)

msg.body = "test bpod"
msg.html = "<h1>Ty</h1>"

mail.send(msg)