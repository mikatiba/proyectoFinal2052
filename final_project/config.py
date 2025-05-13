import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-secreta-flask')

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+mysqldb://root:701512@localhost/consultas_medicas'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False