import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_login import LoginManager

# Inicializa las extensiones fuera de la función create_app para poder
# acceder a ellas en otros archivos si es necesario.
db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'base', 'base.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'be7f4934eff192c308c3b7d14d3550a6'
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 280

    # Configuración de Flask-Mail
    # Configuración del servidor SMTP de Google
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465  # El puerto seguro SSL para Gmail es 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'carnilexplantascarnivoras@gmail.com'  # Coloca tu dirección de correo de Gmail
    app.config['MAIL_PASSWORD'] = ''  # Coloca la contraseña de tu cuenta de Gmail

    # Configuración de Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'main.iniciar_sesion'  # Ruta a la página de inicio de sesión

    # Inicializa las extensiones con la aplicación
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    # Registro del Blueprint en la aplicación
    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        # Importa los modelos aquí para evitar problemas de importación circular
        from . import models
        db.create_all()

    return app
