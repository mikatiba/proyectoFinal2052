import os
from dotenv import load_dotenv

load_dotenv() #carga automáticamente las variables de entorno definidas en un archivo .env. 

#Variables de entorno
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') #Carga el SECRET_KEY ya establecido en otro archivo.

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') #Carga el DATABASE_URL desde otro archivo.

    SQLALCHEMY_TRACK_MODIFICATIONS = False