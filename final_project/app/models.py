from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Carga un usuario desde su ID, necesario para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Modelo de roles (Admin, Médico, Paciente)
class Role(db.Model):
    __tablename__ = 'role'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    users = db.relationship('User', backref='role', lazy=True)

# Modelo de usuarios
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    # Relación con citas donde el usuario es médico o paciente
    citas_como_medico = db.relationship('Cita', foreign_keys='Cita.medico_id', backref='medico', lazy=True)
    citas_como_paciente = db.relationship('Cita', foreign_keys='Cita.paciente_id', backref='paciente', lazy=True)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

# Modelo de citas médicas
class Cita(db.Model):
    __tablename__ = 'cita'

    id = db.Column(db.Integer, primary_key=True)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    motivo = db.Column(db.Text, nullable=False)
    estado = db.Column(db.Enum('Agendada', 'Cancelada', 'Realizada'), default='Agendada', nullable=False)
    observaciones = db.Column(db.Text)