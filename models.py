"""
Modelos de la base de datos para el sistema de gestión de préstamos
"""
from datetime import datetime, date, timedelta
from calendar import monthrange
from database import db
from decimal import Decimal, ROUND_DOWN


def _round_to_cents(value):
    return value.quantize(Decimal('0.01'), rounding=ROUND_DOWN)


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
    
    @staticmethod
    def _sumar_un_mes(fecha):
        if not fecha:
            return None

        year = fecha.year + (fecha.month // 12)
        month = fecha.month % 12 + 1
        last_day = monthrange(year, month)[1]
        day = min(fecha.day, last_day)
        return date(year, month, day)

    @staticmethod
    def _calcular_fecha_vencimiento(fecha):
        if fecha and fecha.weekday() == 6:
            return fecha + timedelta(days=1)
        return fecha

    @staticmethod
    def generar_tabla_amortizacion(monto, tasa_interes, cantidad_cuotas, fecha_desembolso):
        """
        Genera una tabla de amortización conservando el ajuste de centavos
        y aplicándolo de forma acumulada para que la suma cierre exactamente.
        """
        monto = Decimal(str(monto))
        tasa_anual = Decimal(str(tasa_interes))
        cantidad_cuotas = int(cantidad_cuotas)

        tasa_mensual = tasa_anual / Decimal('100') / Decimal('12')
        if tasa_mensual == 0:
            cuota_exacta = monto / Decimal(cantidad_cuotas)
        else:
            factor = (Decimal('1') + tasa_mensual) ** cantidad_cuotas
            cuota_exacta = monto * (tasa_mensual * factor) / (factor - Decimal('1'))

        cuota = _round_to_cents(cuota_exacta)
        saldo = monto
        fecha_actual = fecha_desembolso
        residuo = Decimal('0.00')
        filas = []

        for i in range(1, cantidad_cuotas + 1):
            interes = _round_to_cents(saldo * tasa_mensual)

            if i == cantidad_cuotas:
                # En la última cuota, el capital es el saldo restante exacto
                # más cualquier residuo acumulado por redondeos
                capital = saldo + residuo
                capital = _round_to_cents(capital)
                cuota_periodo = capital + interes
                saldo_restante = Decimal('0.00')
            else:
                capital_bruto = cuota + residuo - interes
                capital = _round_to_cents(capital_bruto)
                residuo = capital_bruto - capital
                saldo_restante = saldo - capital
                cuota_periodo = cuota
                # Actualizar saldo para la siguiente iteración
                saldo = saldo_restante

            if fecha_actual:
                fecha_vencimiento = Prestamo._calcular_fecha_vencimiento(
                    Prestamo._sumar_un_mes(fecha_actual)
                )
            else:
                fecha_vencimiento = None

            filas.append({
                'numero_cuota': i,
                'fecha_vencimiento': fecha_vencimiento,
                'capital': capital,
                'interes': interes,
                'monto_cuota': cuota_periodo,
                'saldo_restante': saldo_restante,
            })
            fecha_actual = fecha_vencimiento

        return filas

    def generar_cronograma(self):
        """
        Genera el cronograma de pagos usando el sistema francés
        con ajuste acumulado de centavos y fechas hábiles.
        """
        filas = self.generar_tabla_amortizacion(
            self.monto,
            self.tasa_interes,
            self.cantidad_cuotas,
            self.fecha_desembolso,
        )

        # Eliminar cuotas existentes
        Cuota.query.filter_by(prestamo_id=self.id).delete()

        for fila in filas:
            cuota_obj = Cuota(
                prestamo_id=self.id,
                numero_cuota=fila['numero_cuota'],
                fecha_vencimiento=fila['fecha_vencimiento'],
                capital=fila['capital'],
                interes=fila['interes'],
                monto_cuota=fila['monto_cuota'],
                saldo_restante=fila['saldo_restante'],
                estado='PENDIENTE'
            )
            db.session.add(cuota_obj)

        self.cuota_mensual = filas[0]['monto_cuota'] if filas else Decimal('0.00')
        self.interes_total = sum((fila['interes'] for fila in filas), Decimal('0.00'))
        self.monto_total = self.monto + self.interes_total

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
