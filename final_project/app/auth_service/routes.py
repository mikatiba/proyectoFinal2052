from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms import LoginForm, RegisterForm
from app.models import db, User, Role
from flask_login import login_user, logout_user, current_user

# ✅ Blueprint corregido
auth = Blueprint('auth', __name__)

@auth.route('/')
def index():
    """
    Página raíz. Redirige al dashboard si el usuario está autenticado, si no al login.
    """
    if current_user.is_authenticated:
        return redirect(url_for('appointments.dashboard'))
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Inicia sesión de un usuario existente si las credenciales son válidas.
    """
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('appointments.dashboard'))

        flash('Credenciales inválidas')

    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registra un nuevo usuario con un rol específico (Admin, Médico, Paciente).
    """
    form = RegisterForm()
    
    if form.validate_on_submit():
        role = Role.query.filter_by(name=form.role.data).first()

        user = User(
            username=form.username.data,
            email=form.email.data,
            role=role
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Usuario registrado exitosamente.')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@auth.route('/logout')
def logout():
    """
    Cierra sesión del usuario actual.
    """
    logout_user()
    return redirect(url_for('auth.index'))