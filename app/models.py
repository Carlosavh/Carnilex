from . import db, bcrypt

class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    password_hash = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, nombre, password, email):
        self.nombre = nombre
        self.password_hash = self.set_password(password)
        self.email = email

    @staticmethod
    def set_password(password):
        return bcrypt.generate_password_hash(password).decode('utf-8')
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

