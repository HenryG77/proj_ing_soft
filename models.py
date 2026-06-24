"""
Modelos de la base de datos para el sistema de gestión de préstamos
"""
from datetime import datetime, date
from database import db
from decimal import Decimal


class Cliente(db.Model):
    """
    Modelo para la tabla de clientes
    """
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    documento = db.Column(db.String(20), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    correo = db.Column(db.String(100))
    direccion = db.Column(db.String(200))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con préstamos
    prestamos = db.relationship('Prestamo', backref='cliente', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Cliente {self.nombre} {self.apellido}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'documento': self.documento,
            'telefono': self.telefono,
            'correo': self.correo,
            'direccion': self.direccion,
            'fecha_registro': self.fecha_registro.strftime('%Y-%m-%d') if self.fecha_registro else None
        }


class Prestamo(db.Model):
    """
    Modelo para la tabla de préstamos
    """
    __tablename__ = 'prestamos'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    monto = db.Column(db.Numeric(12, 2), nullable=False)
    tasa_interes = db.Column(db.Numeric(5, 2), nullable=False)  # Tasa anual en porcentaje
    cantidad_cuotas = db.Column(db.Integer, nullable=False)
    fecha_desembolso = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(20), default='ACTIVO')  # ACTIVO, CANCELADO
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    cuota_mensual = db.Column(db.Numeric(15, 2))
    interes_total = db.Column(db.Numeric(15, 2))
    monto_total = db.Column(db.Numeric(15, 2))
    
    # Relación con cuotas
    cuotas = db.relationship('Cuota', backref='prestamo', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Prestamo {self.id} - Cliente {self.cliente_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'cliente_nombre': f'{self.cliente.nombre} {self.cliente.apellido}' if self.cliente else '',
            'monto': float(self.monto),
            'tasa_interes': float(self.tasa_interes),
            'cantidad_cuotas': self.cantidad_cuotas,
            'fecha_desembolso': self.fecha_desembolso.strftime('%Y-%m-%d') if self.fecha_desembolso else None,
            'estado': self.estado,
            'fecha_creacion': self.fecha_creacion.strftime('%Y-%m-%d') if self.fecha_creacion else None
        }
    
    def calcular_cuota_mensual(self):
        """
        Calcula la cuota mensual usando el sistema francés de amortización
        Fórmula: Cuota = P * [r(1+r)^n] / [(1+r)^n - 1]
        Donde:
        P = Monto del préstamo
        r = Tasa de interés mensual
        n = Número de cuotas
        """
        monto = float(self.monto)
        tasa_anual = float(self.tasa_interes)
        n = self.cantidad_cuotas
        
        # Convertir tasa anual a tasa mensual
        tasa_mensual = tasa_anual / 100 / 12
        
        if tasa_mensual == 0:
            return monto / n
        
        cuota = monto * (tasa_mensual * (1 + tasa_mensual) ** n) / ((1 + tasa_mensual) ** n - 1)
        return round(cuota, 2)
    
    def generar_cronograma(self):
        """
        Genera el cronograma de pagos usando el sistema francés
        """
        monto = float(self.monto)
        tasa_anual = float(self.tasa_interes)
        n = self.cantidad_cuotas
        tasa_mensual = tasa_anual / 100 / 12
        cuota = self.calcular_cuota_mensual()
        
        saldo = monto
        fecha_actual = self.fecha_desembolso
        
        # Eliminar cuotas existentes
        Cuota.query.filter_by(prestamo_id=self.id).delete()
        
        for i in range(1, n + 1):
            # Calcular interés del periodo
            interes = round(saldo * tasa_mensual, 2)
            
            # Calcular capital amortizado
            capital = round(cuota - interes, 2)
            
            # Ajustar última cuota
            if i == n:
                capital = round(saldo, 2)
                cuota = round(capital + interes, 2)
            
            # Calcular saldo restante
            saldo = round(saldo - capital, 2)
            if saldo < 0:
                saldo = 0
            
            # Calcular fecha de vencimiento (sumar un mes)
            if fecha_actual:
                # Avanzar al siguiente mes
                if fecha_actual.month == 12:
                    fecha_vencimiento = date(fecha_actual.year + 1, 1, fecha_actual.day)
                else:
                    fecha_vencimiento = date(fecha_actual.year, fecha_actual.month + 1, fecha_actual.day)
                fecha_actual = fecha_vencimiento
            else:
                fecha_vencimiento = None
            
            # Crear cuota
            cuota_obj = Cuota(
                prestamo_id=self.id,
                numero_cuota=i,
                fecha_vencimiento=fecha_vencimiento,
                capital=capital,
                interes=interes,
                monto_cuota=cuota,
                saldo_restante=saldo,
                estado='PENDIENTE'
            )
            db.session.add(cuota_obj)
        
        db.session.commit()


class Cuota(db.Model):
    """
    Modelo para la tabla de cuotas
    """
    __tablename__ = 'cuotas'
    
    id = db.Column(db.Integer, primary_key=True)
    prestamo_id = db.Column(db.Integer, db.ForeignKey('prestamos.id'), nullable=False)
    numero_cuota = db.Column(db.Integer, nullable=False)
    fecha_vencimiento = db.Column(db.Date)
    capital = db.Column(db.Numeric(12, 2), nullable=False)
    interes = db.Column(db.Numeric(12, 2), nullable=False)
    monto_cuota = db.Column(db.Numeric(12, 2), nullable=False)
    saldo_restante = db.Column(db.Numeric(15, 2), nullable=False)
    estado = db.Column(db.String(20), default='PENDIENTE')  # PENDIENTE, PAGADO
    fecha_pago = db.Column(db.Date)
    
    # Relación con pagos
    pagos = db.relationship('Pago', backref='cuota', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Cuota {self.numero_cuota} - Préstamo {self.prestamo_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'prestamo_id': self.prestamo_id,
            'numero_cuota': self.numero_cuota,
            'fecha_vencimiento': self.fecha_vencimiento.strftime('%Y-%m-%d') if self.fecha_vencimiento else None,
            'capital': float(self.capital),
            'interes': float(self.interes),
            'monto_cuota': float(self.monto_cuota),
            'saldo_restante': float(self.saldo_restante),
            'estado': self.estado,
            'fecha_pago': self.fecha_pago.strftime('%Y-%m-%d') if self.fecha_pago else None
        }


class Pago(db.Model):
    """
    Modelo para la tabla de pagos
    """
    __tablename__ = 'pagos'
    
    id = db.Column(db.Integer, primary_key=True)
    cuota_id = db.Column(db.Integer, db.ForeignKey('cuotas.id'), nullable=False)
    fecha_pago = db.Column(db.DateTime, default=datetime.utcnow)
    monto_pagado = db.Column(db.Numeric(15, 2), nullable=False)
    observacion = db.Column(db.String(200))
    
    def __repr__(self):
        return f'<Pago {self.id} - Cuota {self.cuota_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'cuota_id': self.cuota_id,
            'fecha_pago': self.fecha_pago.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_pago else None,
            'monto_pagado': float(self.monto_pagado),
            'observacion': self.observacion
        }
