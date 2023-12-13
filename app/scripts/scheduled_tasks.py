from flask_mail import Mail
from flask import Flask, flash, redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler
from .email_functions import send_advertisement_email, send_shipping_confirmation_email
from . import create_app

app = create_app()
mail = Mail(app)

# Configurar tarea programada (ejecutará send_advertisement_email cada mes)
scheduler = BackgroundScheduler()
scheduler.add_job(send_advertisement_email, 'cron', month='1-12', day='1', hour='0', minute='0', args=['user@example.com', "¡Descuentos especiales para ti este mes! Visita nuestro sitio web para conocer las ofertas."])
scheduler.start()

@app.route('/finalizar-compra', methods=['POST'])
def finalizar_compra():
    # Lógica para finalizar la compra

    # Obtener el correo electrónico del usuario y el nombre del producto
    user_email = 'user@example.com'  # Aquí deberías obtener el correo electrónico del usuario de la compra
    product_name = 'Planta XYZ'  # Aquí deberías obtener el nombre del producto comprado

    # Enviar correo electrónico de confirmación de envío
    send_shipping_confirmation_email(user_email, product_name)

    flash('¡Compra finalizada! Se ha enviado un correo electrónico de confirmación.', 'success')
    return redirect(url_for('main.index'))

if __name__ == '__main__':
    app.run(debug=True)
