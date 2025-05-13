from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # Importa los blueprints actuales
    from app.auth_service.routes import auth
    from app.appointment_service.routes import appointments

    # Registrar los blueprints
    app.register_blueprint(auth)
    app.register_blueprint(appointments)

    return app