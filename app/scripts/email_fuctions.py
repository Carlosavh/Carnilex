from flask_mail import Message
from flask import current_app
from . import mail

def send_advertisement_email(user_email, advertisement_content):
    with current_app.app_context():
        msg = Message('Publicidad Mensual', recipients=[user_email])
        msg.html = f'<p>{advertisement_content}</p>'
        mail.send(msg)

def send_shipping_confirmation_email(user_email, product_name):
    with current_app.app_context():
        msg = Message('Confirmación de Envío', recipients=[user_email])
        msg.html = f'<p>Sus plantas ({product_name}) han sido enviadas. ¡Gracias por su compra!</p>'
        mail.send(msg)
