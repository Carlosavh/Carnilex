from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_mail import Message
from flask_login import login_user, login_required, logout_user, current_user
from .models import Persona, db
from . import bcrypt, mail, login_manager
from datetime import datetime
import random
import string

# Crea el Blueprint
main = Blueprint('main', __name__)

# Ruta para la página de inicio
@main.route('/')
def index():
    return render_template('index.html')

# Ruta para iniciar sesión
@main.route('/inicio-sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        nombre_usuario = request.form.get('nombre_usuario')
        password = request.form.get('contrasena')

        user = Persona.query.filter_by(nombre=nombre_usuario).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            flash('¡Inicio de sesión exitoso!', 'success')
            print(f'Usuario {user.nombre} inició sesión exitosamente.')
            print(f'Nombre de usuario: {nombre_usuario}')
            print(f'Contraseña ingresada: {password}')
            print(f'Contraseña almacenada: {user.password_hash}')
            return redirect(url_for('main.index'))
        else:
            flash('Error en el inicio de sesión. Verifica tus credenciales.', 'danger')

    return render_template('inicio_sesion.html')

# Ruta para cerrar sesión
@main.route('/cerrar-sesion')
@login_required  # Flask-Login: Requiere que el usuario esté autenticado
def cerrar_sesion():
    logout_user()  # Flask-Login: Cierra la sesión del usuario actual
    flash('¡Has cerrado sesión correctamente!', 'success')
    return redirect(url_for('main.index'))

# Ruta para la página de registro
@main.route('/pagina-de-registro', methods=['GET', 'POST'])
def pagina_de_registro():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not password:
            flash('La contraseña no puede estar vacía.', 'danger')
            return redirect(url_for('main.pagina_de_registro'))

        hashed_password = Persona.set_password(password)

        new_user = Persona(nombre=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('¡Tu cuenta ha sido creada!', 'success')
        return redirect(url_for('main.iniciar_sesion'))

    return render_template('pagina-de-registro.html')

# Ruta para la página de recuperación de contraseña
@main.route('/olvido-contrasena', methods=['GET', 'POST'])
def olvido_contrasena():
    if request.method == 'POST':
        email = request.form.get('email')

        # Busca al usuario por su dirección de correo
        user = Persona.query.filter_by(email=email).first()

        if user:
            # Aquí puedes generar una nueva contraseña o enviar la contraseña existente por correo.
            nueva_contrasena = generar_nueva_contrasena()

            # Actualiza la contraseña en la base de datos
            user.password_hash = bcrypt.generate_password_hash(nueva_contrasena).decode('utf-8')
            db.session.commit()

            # Envía el correo electrónico con la nueva contraseña
            enviar_correo_recuperacion(email, nueva_contrasena)

            flash(f'Se ha enviado un correo de recuperación de contraseña a {email}.', 'info')
        else:
            flash('No se encontró un usuario con esa dirección de correo.', 'danger')

        return redirect(url_for('main.iniciar_sesion'))

    return render_template('olvido.html')

def enviar_correo_recuperacion(destinatario, nueva_contrasena):
    # Configura el mensaje de correo
    mensaje = Message('Recuperación de Contraseña', recipients=[destinatario])
    mensaje.body = f'Su nueva contraseña es: {nueva_contrasena}'

    # Envía el correo electrónico
    mail.send(mensaje)

def generar_nueva_contrasena():
    longitud = 10
    caracteres = string.ascii_letters + string.digits + string.punctuation
    nueva_contrasena = ''.join(random.choice(caracteres) for _ in range(longitud))
    return nueva_contrasena

@login_manager.user_loader
def load_user(user_id):
    return Persona.query.get(int(user_id))