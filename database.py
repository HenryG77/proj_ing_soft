"""
Configuración de la base de datos PostgreSQL
"""
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

db = SQLAlchemy()

def get_database_url():
    """
    Retorna la URL de conexión a la base de datos PostgreSQL
    """
    return os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:postgres@localhost:5432/sistema_prestamo'
    )

def init_db(app):
    """
    Inicializa la base de datos con la aplicación Flask
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
