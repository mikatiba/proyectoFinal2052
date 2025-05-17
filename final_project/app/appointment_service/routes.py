from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import db, Cita, User
from app.forms import ChangePasswordForm, AgendarCitaForm
from datetime import datetime

appointments = Blueprint('appointments', __name__)

@appointments.route('/')
def index():
    return render_template('index.html')

@appointments.route('/dashboard')
@login_required
def dashboard():
    """
    Dashboard según el rol:
    - Admin: ve todas las citas.
    - Médico: ve solo las suyas.
    - Paciente: ve solo sus citas.
    """
    if current_user.role.name == 'Admin':
        citas = Cita.query.all()
    elif current_user.role.name == 'Médico':
        citas = Cita.query.filter_by(medico_id=current_user.id).all()
    elif current_user.role.name == 'Paciente':
        citas = Cita.query.filter_by(paciente_id=current_user.id).all()
    else:
        flash('Rol no reconocido.')
        return redirect(url_for('auth.login'))

    return render_template('dashboard.html', citas=citas)

@appointments.route('/agendar', methods=['GET', 'POST'])
@login_required
def agendar_cita():
    """
    Permite a un paciente agendar una cita con un médico.
    """
    if current_user.role.name != 'Paciente':
        flash('Solo los pacientes pueden agendar citas.')
        return redirect(url_for('appointments.dashboard'))

    form = AgendarCitaForm()
    
    # Cargar médicos al SelectField
    medicos = User.query.join(User.role).filter_by(name='Médico').all()
    form.medico_id.choices = [(m.id, m.username) for m in medicos]

    if form.validate_on_submit():
        cita = Cita(
            fecha_hora=form.fecha_hora.data,
            motivo=form.motivo.data,
            medico_id=form.medico_id.data,
            paciente_id=current_user.id,
            estado='Agendada'
        )
        db.session.add(cita)
        db.session.commit()
        flash('Cita agendada exitosamente.')
        return redirect(url_for('appointments.dashboard'))

    return render_template('agendar_cita.html', form=form)

@appointments.route('/cancelar/<int:id>', methods=['POST'])
@login_required
def cancelar_cita(id):
    """
    Permite cancelar una cita si pertenece al usuario o si es admin.
    """
    cita = Cita.query.get_or_404(id)
    if current_user.role.name == 'Admin' or \
       cita.paciente_id == current_user.id or \
       cita.medico_id == current_user.id:

        cita.estado = 'Cancelada'
        db.session.commit()
        flash('Cita cancelada.')
    else:
        flash('No tienes permiso para cancelar esta cita.')

    return redirect(url_for('appointments.dashboard'))

@appointments.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    """
    Permite a cualquier usuario cambiar su contraseña.
    """
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('Contraseña actual incorrecta.')
            return render_template('cambiar_password.html', form=form)

        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Contraseña actualizada.')
        return redirect(url_for('appointments.dashboard'))

    return render_template('cambiar_password.html', form=form)

@appointments.route('/usuarios')
@login_required
def listar_usuarios():
    """
    Solo los admins pueden ver todos los usuarios.
    """
    if current_user.role.name != 'Admin':
        flash("No tienes permiso para acceder a esta página.")
        return redirect(url_for('appointments.dashboard'))

    usuarios = User.query.join(User.role).all()
    return render_template('usuarios.html', usuarios=usuarios)

@appointments.route('/realizar/<int:id>', methods=['POST'])
@login_required
def marcar_cita_realizada(id):
    """
    Permite marcar una cita como 'Realizada' si el usuario es Admin o el Médico asignado.
    """
    cita = Cita.query.get_or_404(id)

    if current_user.role.name == 'Admin' or \
       (current_user.role.name == 'Médico' and cita.medico_id == current_user.id):

        cita.estado = 'Realizada'
        db.session.commit()
        flash('La cita fue marcada como realizada.', 'success')
    else:
        flash('No tienes permiso para realizar esta acción.', 'danger')

    return redirect(url_for('appointments.dashboard'))