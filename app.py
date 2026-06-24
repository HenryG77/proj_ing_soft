"""
Aplicación Flask para el sistema de gestión de préstamos
"""
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, date
from decimal import Decimal
from database import db, init_db
from models import Cliente, Prestamo, Cuota, Pago

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'

# Inicializar base de datos
init_db(app)


# ==================== Rutas del Dashboard ====================

@app.route('/')
def dashboard():
    """
    Página principal del dashboard con estadísticas
    """
    # Estadísticas generales
    total_clientes = Cliente.query.count()
    total_prestamos = Prestamo.query.count()
    prestamos_activos = Prestamo.query.filter_by(estado='ACTIVO').count()
    
    # Calcular capital prestado total
    capital_prestado = db.session.query(db.func.sum(Prestamo.monto)).scalar() or 0
    
    # Calcular intereses generados (sumando el interés de todas las cuotas pagadas)
    intereses_generados = db.session.query(db.func.sum(Cuota.interes)).join(Pago).filter(Cuota.estado == 'PAGADO').scalar() or 0
    
    # Datos para gráficos
    prestamos_por_estado = db.session.query(
        Prestamo.estado,
        db.func.count(Prestamo.id)
    ).group_by(Prestamo.estado).all()
    
    # Préstamos por mes
    prestamos_por_mes_query = db.session.query(
        db.func.extract('month', Prestamo.fecha_desembolso).label('mes'),
        db.func.extract('year', Prestamo.fecha_desembolso).label('anio'),
        db.func.count(Prestamo.id).label('cantidad'),
        db.func.sum(Prestamo.monto).label('monto')
    ).group_by(
        db.func.extract('year', Prestamo.fecha_desembolso),
        db.func.extract('month', Prestamo.fecha_desembolso)
    ).order_by(
        db.func.extract('year', Prestamo.fecha_desembolso),
        db.func.extract('month', Prestamo.fecha_desembolso)
    )
    prestamos_por_mes = [(row.mes, row.anio, row.cantidad, float(row.monto)) for row in prestamos_por_mes_query.all()]
    
    return render_template('dashboard.html',
                         total_clientes=total_clientes,
                         total_prestamos=total_prestamos,
                         prestamos_activos=prestamos_activos,
                         capital_prestado=float(capital_prestado),
                         intereses_generados=float(intereses_generados),
                         prestamos_por_estado=prestamos_por_estado,
                         prestamos_por_mes=prestamos_por_mes)


# ==================== Rutas de Clientes ====================

@app.route('/clientes')
def clientes():
    """
    Lista todos los clientes
    """
    busqueda = request.args.get('busqueda', '')
    if busqueda:
        clientes = Cliente.query.filter(
            (Cliente.nombre.ilike(f'%{busqueda}%')) |
            (Cliente.apellido.ilike(f'%{busqueda}%')) |
            (Cliente.documento.ilike(f'%{busqueda}%'))
        ).all()
    else:
        clientes = Cliente.query.all()
    
    return render_template('clientes.html', clientes=clientes, busqueda=busqueda)


@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def cliente_nuevo():
    """
    Crea un nuevo cliente
    """
    if request.method == 'POST':
        try:
            cliente = Cliente(
                nombre=request.form['nombre'],
                apellido=request.form['apellido'],
                documento=request.form['documento'],
                telefono=request.form.get('telefono'),
                correo=request.form.get('correo'),
                direccion=request.form.get('direccion')
            )
            db.session.add(cliente)
            db.session.commit()
            flash('Cliente registrado exitosamente', 'success')
            return redirect(url_for('clientes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar cliente: {str(e)}', 'error')
    
    return render_template('clientes.html', modo='crear')


@app.route('/clientes/<int:id>/editar', methods=['GET', 'POST'])
def cliente_editar(id):
    """
    Edita un cliente existente
    """
    cliente = Cliente.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            cliente.nombre = request.form['nombre']
            cliente.apellido = request.form['apellido']
            cliente.documento = request.form['documento']
            cliente.telefono = request.form.get('telefono')
            cliente.correo = request.form.get('correo')
            cliente.direccion = request.form.get('direccion')
            db.session.commit()
            flash('Cliente actualizado exitosamente', 'success')
            return redirect(url_for('clientes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar cliente: {str(e)}', 'error')
    
    return render_template('clientes.html', cliente=cliente, modo='editar')


@app.route('/clientes/<int:id>/eliminar', methods=['POST'])
def cliente_eliminar(id):
    """
    Elimina un cliente
    """
    cliente = Cliente.query.get_or_404(id)
    try:
        db.session.delete(cliente)
        db.session.commit()
        flash('Cliente eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar cliente: {str(e)}', 'error')
    
    return redirect(url_for('clientes'))


# ==================== Rutas de Préstamos ====================

@app.route('/prestamos')
def prestamos():
    """
    Lista todos los préstamos
    """
    estado_filtro = request.args.get('estado', '')
    if estado_filtro:
        prestamos = Prestamo.query.filter_by(estado=estado_filtro).all()
    else:
        prestamos = Prestamo.query.all()
    
    clientes = Cliente.query.all()
    return render_template('prestamos.html', prestamos=prestamos, clientes=clientes, estado_filtro=estado_filtro)


@app.route('/prestamos/nuevo', methods=['GET', 'POST'])
def prestamo_nuevo():
    """
    Crea un nuevo préstamo
    """
    clientes = Cliente.query.all()
    
    if request.method == 'POST':
        try:
            # Convertir monto de formato paraguayo (150.000) a decimal
            monto_str = request.form['monto'].replace('.', '').replace(',', '.')
            prestamo = Prestamo(
                cliente_id=request.form['cliente_id'],
                monto=Decimal(monto_str),
                tasa_interes=Decimal(request.form['tasa_interes']),
                cantidad_cuotas=int(request.form['cantidad_cuotas']),
                fecha_desembolso=datetime.strptime(request.form['fecha_desembolso'], '%Y-%m-%d').date(),
                estado=request.form.get('estado', 'ACTIVO')
            )
            db.session.add(prestamo)
            db.session.commit()
            
            # Generar cronograma de pagos
            prestamo.generar_cronograma()
            
            flash('Préstamo creado exitosamente', 'success')
            return redirect(url_for('prestamos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear préstamo: {str(e)}', 'error')
    
    return render_template('prestamos.html', clientes=clientes, modo='crear')


@app.route('/prestamos/<int:id>')
def prestamo_detalle(id):
    """
    Muestra el detalle de un préstamo
    """
    prestamo = Prestamo.query.get_or_404(id)
    cuotas = Cuota.query.filter_by(prestamo_id=id).order_by(Cuota.numero_cuota).all()
    return render_template('cronograma.html', prestamo=prestamo, cuotas=cuotas)


@app.route('/prestamos/<int:id>/editar', methods=['GET', 'POST'])
def prestamo_editar(id):
    """
    Edita un préstamo existente
    """
    prestamo = Prestamo.query.get_or_404(id)
    clientes = Cliente.query.all()
    
    if request.method == 'POST':
        try:
            # Convertir monto de formato paraguayo (150.000) a decimal
            monto_str = request.form['monto'].replace('.', '').replace(',', '.')
            prestamo.cliente_id = request.form['cliente_id']
            prestamo.monto = Decimal(monto_str)
            prestamo.tasa_interes = Decimal(request.form['tasa_interes'])
            prestamo.cantidad_cuotas = int(request.form['cantidad_cuotas'])
            prestamo.fecha_desembolso = datetime.strptime(request.form['fecha_desembolso'], '%Y-%m-%d').date()
            prestamo.estado = request.form.get('estado', 'ACTIVO')
            db.session.commit()
            
            # Regenerar cronograma de pagos
            prestamo.generar_cronograma()
            
            flash('Préstamo actualizado exitosamente', 'success')
            return redirect(url_for('prestamos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar préstamo: {str(e)}', 'error')
    
    return render_template('prestamos.html', prestamo=prestamo, clientes=clientes, modo='editar')


@app.route('/prestamos/<int:id>/eliminar', methods=['POST'])
def prestamo_eliminar(id):
    """
    Elimina un préstamo
    """
    prestamo = Prestamo.query.get_or_404(id)
    try:
        db.session.delete(prestamo)
        db.session.commit()
        flash('Préstamo eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar préstamo: {str(e)}', 'error')
    
    return redirect(url_for('prestamos'))


# ==================== Rutas de Reportes ====================

@app.route('/reportes')
def reportes():
    """
    Página de reportes con listado de préstamos
    """
    prestamos = Prestamo.query.order_by(Prestamo.fecha_creacion.desc()).all()
    return render_template('reportes.html', prestamos=prestamos)


@app.route('/consultas')
def consultas():
    """
    Página de consultas/extracto con filtros por cliente y estado
    """
    cliente_id = request.args.get('cliente_id', '')
    estado_filtro = request.args.get('estado', '')
    
    prestamos = Prestamo.query
    if cliente_id:
        prestamos = prestamos.filter_by(cliente_id=cliente_id)
    if estado_filtro:
        prestamos = prestamos.filter_by(estado=estado_filtro)
    
    prestamos = prestamos.order_by(Prestamo.fecha_creacion.desc()).all()
    clientes = Cliente.query.all()
    
    return render_template('consultas.html', 
                         prestamos=prestamos, 
                         clientes=clientes, 
                         cliente_id=cliente_id, 
                         estado_filtro=estado_filtro)


# ==================== Rutas de Pagos ====================

@app.route('/cuotas/<int:id>/pagar', methods=['POST'])
def cuota_pagar(id):
    """
    Registra el pago de una cuota
    """
    cuota = Cuota.query.get_or_404(id)
    
    if cuota.estado == 'PAGADO':
        flash('Esta cuota ya ha sido pagada', 'warning')
        return redirect(url_for('prestamo_detalle', id=cuota.prestamo_id))
    
    try:
        # Crear registro de pago
        pago = Pago(
            cuota_id=cuota.id,
            fecha_pago=datetime.utcnow(),
            monto_pagado=cuota.monto_cuota
        )
        db.session.add(pago)
        
        # Marcar cuota como pagada
        cuota.estado = 'PAGADO'
        cuota.fecha_pago = date.today()
        
        # Verificar si todas las cuotas están pagadas para cambiar estado del préstamo
        prestamo = cuota.prestamo
        todas_pagadas = all(c.estado == 'PAGADO' for c in prestamo.cuotas)
        if todas_pagadas:
            prestamo.estado = 'CANCELADO'
        
        db.session.commit()
        flash('Pago registrado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al registrar pago: {str(e)}', 'error')
    
    return redirect(url_for('prestamo_detalle', id=cuota.prestamo_id))


@app.route('/api/calcular-cuota', methods=['POST'])
def api_calcular_cuota():
    """
    API para calcular la cuota mensual
    """
    data = request.json
    monto = float(data.get('monto', 0))
    tasa_interes = float(data.get('tasa_interes', 0))
    cantidad_cuotas = int(data.get('cantidad_cuotas', 1))
    
    # Calcular cuota usando el sistema francés
    tasa_mensual = tasa_interes / 100 / 12
    
    if tasa_mensual == 0:
        cuota = monto / cantidad_cuotas
    else:
        cuota = monto * (tasa_mensual * (1 + tasa_mensual) ** cantidad_cuotas) / ((1 + tasa_mensual) ** cantidad_cuotas - 1)
    
    return jsonify({'cuota': round(cuota, 2)})


# ==================== Manejo de Errores ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('base.html', error='Página no encontrada'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('base.html', error='Error del servidor'), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
