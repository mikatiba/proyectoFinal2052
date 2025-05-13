from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, DateTimeLocalField 
from wtforms.validators import DataRequired, Email, EqualTo, Length

# Formulario para login de usuario
class LoginForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

# Formulario para registrar un nuevo usuario (Admin, Médico o Paciente)
class RegisterForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])
    
    role = SelectField(
        'Rol',
        choices=[('Admin', 'Admin'), ('Médico', 'Médico'), ('Paciente', 'Paciente')],
        validators=[DataRequired()]
    )

    submit = SubmitField('Registrarse')

# Formulario para cambiar la contraseña del usuario
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Contraseña actual', validators=[DataRequired()])
    new_password = PasswordField('Nueva contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar nueva contraseña', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Actualizar contraseña')

# Formulario para agendar una cita médica
class AgendarCitaForm(FlaskForm):
    fecha_hora = DateTimeLocalField(
        'Fecha y Hora',
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired()]
    )
    motivo = TextAreaField('Motivo', validators=[DataRequired()])
    medico_id = SelectField('Médico', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Agendar')