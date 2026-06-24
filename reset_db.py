"""
Script para eliminar y recrear las tablas de la base de datos
"""
from database import db, init_db
from models import Cliente, Prestamo, Cuota, Pago
from app import app

with app.app_context():
    # Eliminar todas las tablas
    db.drop_all()
    print("Tablas eliminadas exitosamente")
    
    # Crear todas las tablas
    db.create_all()
    print("Tablas creadas exitosamente")
