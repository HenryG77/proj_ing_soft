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


def normalizar_valor_numerico(valor):
    """Normaliza un string numérico con separadores de miles o decimales."""
    if valor is None:
        return Decimal('0')

    texto = str(valor).strip().replace(' ', '')
    if texto == '':
        return Decimal('0')

    if ',' in texto and '.' in texto:
        texto = texto.replace('.', '').replace(',', '.')
    elif ',' in texto:
        texto = texto.replace(',', '.')
    elif '.' in texto:
        partes = texto.split('.')
        if len(partes[-1]) > 2:
            texto = ''.join(partes)

    try:
        return Decimal(texto)
    except Exception:
        return Decimal('0')

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
            monto_str = request.form['monto']
            prestamo = Prestamo(
                cliente_id=request.form['cliente_id'],
                monto=normalizar_valor_numerico(monto_str),
                tasa_interes=normalizar_valor_numerico(request.form['tasa_interes']),
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
    
    return render_template('prestamos.html', clientes=clientes, modo='crear', fecha_hoy=date.today().strftime('%Y-%m-%d'))


@app.route('/prestamos/<int:id>')
def prestamo_detalle(id):
    """
    Muestra el detalle de un préstamo
    """
    prestamo = Prestamo.query.get_or_404(id)
    cuotas = Cuota.query.filter_by(prestamo_id=id).order_by(Cuota.numero_cuota).all()
    # Pasar la fecha de hoy para calcular días de atraso en la plantilla
    return render_template('cronograma.html', prestamo=prestamo, cuotas=cuotas, hoy=date.today())


@app.route('/prestamos/<int:id>/general')
def prestamo_general(id):
    """
    Muestra la vista General con movimientos de crédito/débito y saldo.
    """
    prestamo = Prestamo.query.get_or_404(id)
    cuotas = Cuota.query.filter_by(prestamo_id=id).order_by(Cuota.numero_cuota).all()

    saldo = float(prestamo.monto or 0)
    filas = [
        {
            'sec': 1,
            'fecha': prestamo.fecha_desembolso,
            'movimiento': 'Desembolso',
            'credito': float(prestamo.monto or 0),
            'debito': None,
            'saldo': saldo,
            'interes': None,
        }
    ]

    sec = 2
    for cuota in cuotas:
        pagos_list = list(cuota.pagos) if cuota.pagos else []
        monto_pagado = sum((float(p.monto_pagado) for p in pagos_list)) if pagos_list else 0.0
        if monto_pagado <= 0:
            continue

        fecha_pago = None
        if pagos_list:
            fecha_pago_dt = max((p.fecha_pago for p in pagos_list if p.fecha_pago))
            fecha_pago = fecha_pago_dt.date() if fecha_pago_dt else cuota.fecha_vencimiento
        else:
            fecha_pago = cuota.fecha_vencimiento

        interes = float(cuota.interes or 0)
        amortizacion = max(0.0, monto_pagado - interes)
        saldo = max(0.0, saldo - amortizacion)

        filas.append({
            'sec': sec,
            'fecha': fecha_pago,
            'movimiento': f'Amortización Cuota N.º {cuota.numero_cuota}',
            'credito': None,
            'debito': monto_pagado,
            'saldo': saldo,
            'interes': interes,
        })
        sec += 1

    return render_template('general.html', prestamo=prestamo, filas=filas)


@app.route('/prestamos/<int:id>/extracto')
def prestamo_extracto(id):
    """
    Muestra el extracto del préstamo con columnas detalladas
    """
    prestamo = Prestamo.query.get_or_404(id)
    cuotas = Cuota.query.filter_by(prestamo_id=id).order_by(Cuota.numero_cuota).all()
    hoy = date.today()

    # Preparar filas con los campos solicitados
    filas = []
    monto_total = float(prestamo.monto)
    running_paid_capital = 0.0

    total_capital_plan = 0.0
    total_pago_plan = 0.0
    total_cuota = 0.0
    total_int_cuotas = 0.0
    total_int_pago = 0.0

    # Construir mapa de pagos por cuota para sumar montos pagados
    for cuota in cuotas:
        capital_plan = float(cuota.capital or 0)
        pago_plan = 0.0  # importe total ya pagado del capital (por esta cuota)
        int_cuotas = float(cuota.interes or 0)
        fecha_venc = cuota.fecha_vencimiento
        fecha_pago = None

        # Monto pagado total registrado en pagos asociados (suma de pagos sobre esta cuota)
        pagos_list = list(cuota.pagos) if cuota.pagos else []
        monto_pagado = sum((float(p.monto_pagado) for p in pagos_list)) if pagos_list else 0.0

        # Fecha de pago: tomar la última fecha registrada en pagos, si existe
        if pagos_list:
            fecha_pago_dt = max((p.fecha_pago for p in pagos_list))
            fecha_pago = fecha_pago_dt.date() if fecha_pago_dt else None
        elif cuota.fecha_pago:
            fecha_pago = cuota.fecha_pago

        # Interés efectivamente cobrado: asumimos que los primeros importes pagados cubren interés hasta el monto de la cuota de interés
        int_pago = 0.0
        restante = monto_pagado
        if restante > 0:
            int_pago = min(int_cuotas, restante)
            restante = max(0.0, restante - int_pago)

        # Capital efectivamente pagado para esta cuota (lo que queda después de cubrir interés)
        pago_plan = min(capital_plan, restante)

        # Actualizar saldo real de capital pendiente acumulando capital pagado
        running_paid_capital += pago_plan

        saldo_capital = monto_total - running_paid_capital

        # Días: diferencia entre fecha de pago (si existe) o hoy y la fecha de vencimiento
        dias = None
        if fecha_venc:
            ref = fecha_pago if fecha_pago else hoy
            dias = (ref - fecha_venc).days

        cuota_val = capital_plan + int_cuotas

        filas.append({
            'numero': cuota.numero_cuota,
            'fecha_vencimiento': fecha_venc,
            'capital_plan': capital_plan,
            'pago_plan': pago_plan,
            'cuota': cuota_val,
            'saldo_capital': saldo_capital,
            'int_cuotas': int_cuotas,
            'int_pago': int_pago,
            'dias': dias,
            'fecha_pago': fecha_pago,
            'monto_pagado': monto_pagado,
        })

        total_capital_plan += capital_plan
        total_pago_plan += pago_plan
        total_cuota += cuota_val
        total_int_cuotas += int_cuotas
        total_int_pago += int_pago

    totales = {
        'capital_plan': total_capital_plan,
        'pago_plan': total_pago_plan,
        'cuota': total_cuota,
        'int_cuotas': total_int_cuotas,
        'int_pago': total_int_pago,
    }

    return render_template('extracto.html', prestamo=prestamo, filas=filas, totales=totales, hoy=hoy)


@app.route('/prestamos/<int:id>/editar', methods=['GET', 'POST'])
def prestamo_editar(id):
    """
    Edita un préstamo existente
    """
    prestamo = Prestamo.query.get_or_404(id)
    clientes = Cliente.query.all()
    
    if request.method == 'POST':
        try:
            monto_str = request.form['monto']
            prestamo.cliente_id = request.form['cliente_id']
            prestamo.monto = normalizar_valor_numerico(monto_str)
            prestamo.tasa_interes = normalizar_valor_numerico(request.form['tasa_interes'])
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


@app.route('/pagos')
def pagos():
    """
    Página de pagos que lista préstamos con filtros.
    """
    cliente_id = request.args.get('cliente_id', '')
    prestamo_id = request.args.get('prestamo_id', '')
    estado = request.args.get('estado', '')

    prestamos_query = Prestamo.query
    if cliente_id:
        prestamos_query = prestamos_query.filter_by(cliente_id=cliente_id)
    if prestamo_id:
        prestamos_query = prestamos_query.filter_by(id=prestamo_id)
    if estado:
        prestamos_query = prestamos_query.filter_by(estado=estado)

    prestamos = prestamos_query.order_by(Prestamo.fecha_creacion.desc()).all()
    clientes = Cliente.query.all()

    return render_template('pagos.html', clientes=clientes, prestamos=prestamos, cliente_id=cliente_id, prestamo_id=prestamo_id, estado=estado)


@app.route('/pagos/prestamo/<int:prestamo_id>')
def pagos_prestamo(prestamo_id):
    """
    Muestra las cuotas pendientes de un préstamo seleccionado.
    """
    prestamo = Prestamo.query.get_or_404(prestamo_id)
    cuotas_pendientes = Cuota.query.filter_by(prestamo_id=prestamo_id).filter(Cuota.estado != 'PAGADO').order_by(Cuota.numero_cuota).all()
    return render_template('pagos_detalle.html', prestamo=prestamo, cuotas_pendientes=cuotas_pendientes)


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
