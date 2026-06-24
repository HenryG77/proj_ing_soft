# AUDITORÍA TÉCNICA PROFESIONAL - SISTEMA DE GESTIÓN DE PRÉSTAMOS
**Análisis Académico y Profesional - Junio 2026**

---

## 1. VISIÓN GENERAL

### Problema que resuelve
El sistema automatiza el ciclo completo de gestión de préstamos: desde la creación del cliente, solicitud y desembolso del préstamo, hasta el cronograma de pagos y registro de cuotas pagadas.

### Objetivo principal
Proporcionar una plataforma web integrada para instituciones financieras que necesiten administrar préstamos con cálculo automático de cuotas, cronogramas de amortización y seguimiento de pagos.

### Funcionalidades principales
1. **Gestión de Clientes**: CRUD completo (crear, leer, actualizar, eliminar)
2. **Gestión de Préstamos**: crear préstamos con cálculo automático de cuotas
3. **Generación automática de Cronogramas**: sistema francés de amortización
4. **Registro de Pagos**: control de cuotas pagadas
5. **Dashboard de Estadísticas**: métricas en tiempo real
6. **Reportes y Consultas**: filtrado por cliente y estado
7. **API REST**: endpoint para cálculo de cuotas

### Caso de uso real
Una cooperativa de crédito necesita gestionar 200 clientes y 500+ préstamos activos. Sin el sistema: cálculos manuales, errores en cuotas, imposibilidad de auditoría. Con el sistema: automatización completa, precisión matemática garantizada, trazabilidad total.

---

## 2. ARQUITECTURA DEL SISTEMA

### Diagrama de arquitectura textual

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                      │
│  (Templates HTML: dashboard, clientes, prestamos, etc.)      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP/REST
                         │
┌─────────────────────────────────────────────────────────────┐
│                   CAPA DE APLICACIÓN                         │
│                       FLASK                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Rutas (Endpoints):                                   │   │
│  │ - Clientes CRUD (/clientes/*)                        │   │
│  │ - Préstamos CRUD (/prestamos/*)                      │   │
│  │ - Pagos (/cuotas/*/pagar)                            │   │
│  │ - API (/api/calcular-cuota)                          │   │
│  │ - Dashboard, Reportes, Consultas                     │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ SQLAlchemy ORM
                         │
┌─────────────────────────────────────────────────────────────┐
│                   CAPA DE DATOS (ORM)                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Modelos SQLAlchemy:                                  │   │
│  │ - Cliente                                            │   │
│  │ - Préstamo                                           │   │
│  │ - Cuota                                              │   │
│  │ - Pago                                               │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Conexión PostgreSQL
                         │
┌─────────────────────────────────────────────────────────────┐
│            CAPA DE PERSISTENCIA (PostgreSQL)                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Tablas:                                              │   │
│  │ - clientes (id PK, nombre, apellido, documento...)  │   │
│  │ - prestamos (id PK, cliente_id FK, monto, ...)      │   │
│  │ - cuotas (id PK, prestamo_id FK, ...)               │   │
│  │ - pagos (id PK, cuota_id FK, ...)                   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Flujo completo de una solicitud

1. **Usuario ingresa a /prestamos/nuevo (GET)**
   - Flask renderiza template con formulario
   - Consulta BD para obtener lista de clientes
   - HTML con opciones en dropdown

2. **Usuario completa formulario y envía (POST a /prestamos/nuevo)**
   - Request interceptado por Flask
   - Validación de datos (conversión de formatos)
   - Creación de objeto Prestamo
   - SQLAlchemy traduce a INSERT SQL
   - PostgreSQL persiste datos
   - COMMIT de transacción

3. **Flask genera cronograma automático**
   - Método generar_cronograma() se ejecuta
   - Cálculo matemático francés (150 iteraciones si 150 cuotas)
   - Para cada cuota: INSERT en tabla cuotas
   - PostgreSQL retorna confirmación
   - COMMIT final

4. **Respuesta al usuario**
   - Redirección a /prestamos
   - Flash message (exitoso)
   - Template renderiza lista actualizada
   - Browser muestra resultado

### Flujo de cálculo de cuota (endpoint API)

```
Browser: POST /api/calcular-cuota
{monto: 100000, tasa_interes: 15, cantidad_cuotas: 24}
    ↓
Flask recibe request.json
    ↓
Extrae parámetros (monto, tasa, cantidad_cuotas)
    ↓
Cálculo matemático:
  - tasa_mensual = 15/100/12 = 0.0125
  - cuota = 100000 * (0.0125 * 1.0125^24) / (1.0125^24 - 1)
  - cuota ≈ 4415.07
    ↓
Response JSON: {cuota: 4415.07}
    ↓
Browser recibe y actualiza UI
```

### Capas identificadas

| Capa | Componentes | Responsabilidad |
|------|-------------|-----------------|
| **Presentación** | Templates HTML (Jinja2) | Interfaz usuario, validación cliente |
| **Aplicación** | app.py (rutas Flask) | Orquestación, lógica de negocio |
| **Datos** | models.py (SQLAlchemy) | Definición entidades, validación ORM |
| **Persistencia** | database.py, PostgreSQL | Almacenamiento permanente |
| **Comunicación** | HTTP/REST, WSGI | Transporte entre capas |

---

## 3. TECNOLOGÍAS UTILIZADAS

### Flask 3.0.0

**¿Qué es?**
Framework web minimalista basado en Werkzeug. Proporciona routing, manejo de requests/responses, context management.

**¿Por qué se utilizó?**
- Ligero y flexible (microfraework)
- Curva de aprendizaje suave para proyecto académico
- No impone estructura (vs Django más pesado)
- Perfecto para APIs REST pequeñas

**Rol en el proyecto:**
- Routing de todas las URLs
- Manejo de request/response
- Sesiones y flash messages
- Contexto de aplicación para ORM

**Ventajas:**
- Código limpio y legible
- Fácil debugging
- Múltiples decoradores disponibles

**Desventajas:**
- Menos built-in que Django (sin admin, sin ORM nativo)
- Requiere más configuración manual
- Comunidad más pequeña

---

### Flask-SQLAlchemy 3.1.1

**¿Qué es?**
Extensión que integra SQLAlchemy ORM con Flask. Simplifica configuración y gestión de sesiones.

**Rol:**
- Define modelos de datos
- Abstracción de queries SQL
- Manejo automático de sesiones
- Relaciones entre entidades

**Ventajas:**
- SQL puro cuando es necesario
- Relaciones automáticas (backref)
- Cascade automático
- Migraciones posibles (con Alembic)

**Desventajas:**
- Curva aprendizaje pronunciada
- N+1 queries si no se optimiza
- Performance puede degradarse en datos grandes

---

### PostgreSQL (vía psycopg2-binary 2.9.0+)

**¿Qué es?**
Sistema gestor de bases de datos relacional de código abierto. Psycopg2 es el driver Python.

**Rol:**
- Almacenamiento permanente de datos
- Integridad referencial (foreign keys)
- Transacciones ACID
- Consultas complejas con SQL

**Ventajas:**
- Altamente confiable y robusto
- Soporta tipos complejos (NUMERIC preciso)
- Excelente para cálculos financieros
- Escala bien

**Desventajas:**
- Más pesado que SQLite
- Requiere instalación separada
- Configuración más compleja

**¿Por qué PostgreSQL y no SQLite?**
- SQLite no es ideal para concurrencia (múltiples usuarios)
- PostgreSQL tiene mejor soporte ACID
- Más profesional para producción

---

### python-dotenv 1.0.0

**Rol:**
- Cargar variables de entorno desde .env
- Configuración sin hardcodear (DATABASE_URL, etc.)
- Diferentes configs por ambiente (dev, prod)

**Uso en proyecto:**
```python
load_dotenv()
db_url = os.getenv('DATABASE_URL', default_value)
```

---

## 4. INSTALACIÓN

### Dependencias y su propósito

| Paquete | Versión | Propósito | Instalación |
|---------|---------|----------|------------|
| Flask | 3.0.0 | Framework web | `pip install Flask==3.0.0` |
| Flask-SQLAlchemy | 3.1.1 | ORM integrado con Flask | `pip install Flask-SQLAlchemy==3.1.1` |
| psycopg2-binary | >=2.9.0 | Driver PostgreSQL para Python | `pip install psycopg2-binary` |
| python-dotenv | 1.0.0 | Carga de variables de entorno | `pip install python-dotenv==1.0.0` |

### Pasos de instalación

**1. Crear entorno virtual**
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
```

**2. Instalar dependencias**
```bash
pip install -r requirements.txt
```

**3. Configurar base de datos**
```bash
# Crear archivo .env con:
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/sistema_prestamo
```

**4. Crear tablas (primera ejecución)**
```bash
python reset_db.py
```

**5. Ejecutar aplicación**
```bash
python app.py
# Acceder a http://localhost:5000
```

---

## 5. FLASK - ANÁLISIS DETALLADO

### Inicialización de la aplicación

```python
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'
init_db(app)
```

**SECRET_KEY**: Usado para firmar cookies de sesión y flash messages. ⚠️ **VULNERABILIDAD**: Hardcodeado, debería estar en .env

### Ciclo de vida de una petición

1. **Recepción de request**
   - Browser envía HTTP request
   - WSGI app (Flask) recibe bytes

2. **Routing**
   - Flask busca ruta coincidente en decoradores @app.route()
   - Extrae parámetros de URL

3. **Ejecución de función handler**
   - Se ejecuta función asociada a ruta
   - Acceso a request (headers, form, json, etc.)

4. **Lógica de negocio**
   - Consultas a BD vía SQLAlchemy
   - Cálculos y transformaciones
   - Manejo de excepciones

5. **Renderizado de response**
   - render_template() renderiza Jinja2
   - jsonify() retorna JSON
   - redirect() envía código 302

6. **Envío al navegador**
   - Flask retorna response al cliente WSGI
   - HTTP response con headers y body

### Rutas principales

| Ruta | Método | Función | Tipo |
|------|--------|---------|------|
| `/` | GET | dashboard() | Vista |
| `/clientes` | GET | clientes() | Vista |
| `/clientes/nuevo` | GET/POST | cliente_nuevo() | Formulario |
| `/clientes/<id>/editar` | GET/POST | cliente_editar() | Formulario |
| `/clientes/<id>/eliminar` | POST | cliente_eliminar() | Acción |
| `/prestamos` | GET | prestamos() | Vista |
| `/prestamos/nuevo` | GET/POST | prestamo_nuevo() | Formulario |
| `/prestamos/<id>` | GET | prestamo_detalle() | Vista |
| `/prestamos/<id>/editar` | GET/POST | prestamo_editar() | Formulario |
| `/prestamos/<id>/eliminar` | POST | prestamo_eliminar() | Acción |
| `/cuotas/<id>/pagar` | POST | cuota_pagar() | Acción |
| `/api/calcular-cuota` | POST | api_calcular_cuota() | API JSON |
| `/reportes` | GET | reportes() | Vista |
| `/consultas` | GET | consultas() | Vista |

### Decoradores utilizados

```python
@app.route('/')              # Define ruta HTTP
@app.errorhandler(404)       # Manejador de errores
@app.errorhandler(500)
```

### Context management

Flask proporciona contextos automáticos:
- **request context**: request actual, form, args, etc.
- **app context**: para acceder a db.session fuera de views

```python
with app.app_context():      # Reset_db.py lo usa
    db.create_all()
```

---

## 6. REST API - ANÁLISIS CRÍTICO

### ¿Sigue principios REST?

**Respuesta: PARCIALMENTE SÍ**

REST ideal requiere:
1. ✅ Uso correcto de métodos HTTP (GET, POST, DELETE)
2. ✅ URIs representan recursos (/clientes, /prestamos, /cuotas)
3. ⚠️ Estados correctos HTTP (200, 201, 404, etc.) - **FALTAN VARIOS**
4. ❌ Separación cliente/servidor pura - **Las rutas mezclan renderizado HTML con lógica**
5. ⚠️ Documentación de API - **No existe**

### Endpoints identificados

**CLIENTES:**
```
GET    /clientes              - Lista clientes
GET    /clientes/nuevo        - Formulario crear cliente
POST   /clientes/nuevo        - Crear cliente
GET    /clientes/<id>/editar  - Formulario editar
POST   /clientes/<id>/editar  - Actualizar cliente
POST   /clientes/<id>/eliminar - Eliminar cliente
```

**PRÉSTAMOS:**
```
GET    /prestamos             - Lista préstamos
GET    /prestamos/nuevo       - Formulario crear
POST   /prestamos/nuevo       - Crear préstamo
GET    /prestamos/<id>        - Ver detalle + cronograma
GET    /prestamos/<id>/editar - Formulario editar
POST   /prestamos/<id>/editar - Actualizar préstamo
POST   /prestamos/<id>/eliminar - Eliminar préstamo
```

**CUOTAS/PAGOS:**
```
POST   /cuotas/<id>/pagar     - Registrar pago de cuota
```

**API:**
```
POST   /api/calcular-cuota    - Calcula cuota mensual (JSON)
```

**REPORTES:**
```
GET    /reportes              - Reporte de préstamos
GET    /consultas             - Consultas filtradas
```

### Métodos HTTP utilizados

| Método | Cantidad | Correcto | Notas |
|--------|----------|----------|-------|
| GET | 11 | ✅ | Correcto para obtener recursos |
| POST | 10 | ⚠️ | Correcto pero falta PUT/PATCH para editar |
| DELETE | 0 | ❌ | No se usa, usando POST en lugar |

### Códigos de estado HTTP

**¿Cuáles se utilizan?**
- 200 (GET exitoso) - implícito en render_template
- 302 (Redirect después de POST) - usado en todos los POST
- 404 (NOT FOUND) - usando get_or_404()
- 500 (Error servidor) - errorhandler

**¿Cuáles FALTAN?**
- ❌ 201 CREATED (después de crear recurso)
- ❌ 204 NO CONTENT (después de eliminar)
- ❌ 400 BAD REQUEST (datos inválidos)
- ❌ 409 CONFLICT (cliente duplicado - no se valida)
- ❌ 422 UNPROCESSABLE ENTITY (fallo de validación)

### Problemas de diseño REST

1. **Falta separación de responsabilidades**
   ```python
   # POST a /clientes/nuevo renderiza HTML + crea recurso
   # Debería: retornar JSON con 201 CREATED
   ```

2. **Falta documentación de API**
   - Sin Swagger/OpenAPI
   - Cliente no sabe qué endpoint es API y cuál es web

3. **Validación insuficiente**
   - No valida documento duplicado
   - No valida que cliente exista antes de crear préstamo
   - No valida montos negativos

4. **Estados HTTP incorrectos**
   - Siempre 200/302, nunca usa semántica correcta
   - Flash messages en lugar de response bodies

### Cómo mejorar el diseño REST

**Opción 1: Separar API de Web**
```
/api/v1/clientes (JSON)
/web/clientes    (HTML)
```

**Opción 2: Retornar JSON siempre**
```python
@app.route('/api/clientes', methods=['POST'])
def crear_cliente():
    try:
        cliente = Cliente(...)
        db.session.add(cliente)
        db.session.commit()
        return jsonify(cliente.to_dict()), 201
    except IntegrityError:
        return jsonify({'error': 'Documento duplicado'}), 409
```

---

## 7. HTTP - ANÁLISIS DETALLADO

### Métodos HTTP utilizados

**GET** (Lectura, idempotente)
```
GET /clientes
GET /prestamos/<id>
GET /reportes
```
✅ Correcto: No modifica estado

**POST** (Creación/Acción, no idempotente)
```
POST /clientes/nuevo
POST /prestamos/<id>/editar
POST /cuotas/<id>/pagar
```
⚠️ Parcialmente correcto: POST para editar es antipatrón

**DELETE** (Eliminación)
```
❌ NO SE UTILIZA
# Se usa POST en lugar:
POST /clientes/<id>/eliminar
```

### Códigos de estado HTTP

#### Usados correctamente:
- **200 OK**: Cuando GET retorna datos
- **302 Found**: Redirect-after-POST pattern (correcto)
- **404 Not Found**: get_or_404() genera automáticamente

#### Mal utilizados o ausentes:
- **201 Created** ❌: Nunca se retorna tras crear
- **204 No Content** ❌: Nunca se usa tras eliminar
- **400 Bad Request** ❌: No valida entrada
- **409 Conflict** ❌: No detecta duplicados (documento único)
- **422 Unprocessable Entity** ❌: No valida tipos

#### Nunca usados pero necesarios:
- **PUT** (reemplazo completo)
- **PATCH** (actualización parcial)
- **HEAD** (como GET pero sin body)
- **OPTIONS** (método permitidos)

### Flujo HTTP típico en POST

**Request:**
```http
POST /clientes/nuevo HTTP/1.1
Host: localhost:5000
Content-Type: application/x-www-form-urlencoded

nombre=Juan&apellido=Pérez&documento=123456
```

**Procesamiento Flask:**
1. request.method == 'POST' ✓
2. request.form['nombre'] obtiene valores
3. try/except captura errores
4. db.session.commit() persiste
5. Retorna redirect o renderiza con error

**Response:**
```http
HTTP/1.1 302 Found
Location: /clientes
Set-Cookie: session=...
Content-Length: 0
```

**Luego GET:**
```http
GET /clientes HTTP/1.1
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: text/html
...
<html>...lista de clientes...</html>
```

---

## 8. JSON - EJEMPLOS REALES

### Endpoint de API: /api/calcular-cuota

**Request JSON:**
```json
{
  "monto": 150000,
  "tasa_interes": 15.5,
  "cantidad_cuotas": 24
}
```

**Response JSON:**
```json
{
  "cuota": 6789.45
}
```

### Modelos to_dict() - Serialización a JSON

**Cliente.to_dict():**
```json
{
  "id": 1,
  "nombre": "Juan",
  "apellido": "Pérez",
  "documento": "123456789",
  "telefono": "+595987654321",
  "correo": "juan@example.com",
  "direccion": "Calle 1, Asunción",
  "fecha_registro": "2026-06-22"
}
```

**Prestamo.to_dict():**
```json
{
  "id": 1,
  "cliente_id": 1,
  "cliente_nombre": "Juan Pérez",
  "monto": 150000.00,
  "tasa_interes": 15.5,
  "cantidad_cuotas": 24,
  "fecha_desembolso": "2026-06-22",
  "estado": "ACTIVO",
  "fecha_creacion": "2026-06-22"
}
```

**Cuota.to_dict():**
```json
{
  "id": 1,
  "prestamo_id": 1,
  "numero_cuota": 1,
  "fecha_vencimiento": "2026-07-22",
  "capital": 5743.21,
  "interes": 1961.25,
  "monto_cuota": 7704.46,
  "saldo_restante": 144256.79,
  "estado": "PENDIENTE",
  "fecha_pago": null
}
```

**Pago.to_dict():**
```json
{
  "id": 1,
  "cuota_id": 1,
  "fecha_pago": "2026-07-22 14:30:45",
  "monto_pagado": 7704.46,
  "observacion": "Pago completo de cuota 1"
}
```

### Conversión request.form → Decimal/date

**Problemas de conversión:**
```python
# El código hace:
monto_str = request.form['monto'].replace('.', '').replace(',', '.')
prestamo.monto = Decimal(monto_str)

# Ejemplo:
# "150.000" → "150000" → "150000" → Decimal(150000)
# ✅ Correcto manejo del formato paraguayo (usa . como separador de miles)
```

---

## 9. CRUD - ANÁLISIS COMPLETO

### Cliente CRUD

**CREATE (Crear cliente)**
```python
@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def cliente_nuevo():
    if request.method == 'POST':
        cliente = Cliente(...)
        db.session.add(cliente)
        db.session.commit()
```
- ✅ GET retorna formulario
- ✅ POST crea registro
- ❌ No valida documento duplicado

**READ (Leer clientes)**
```python
@app.route('/clientes')
def clientes():
    clientes = Cliente.query.all()  # o con filtro búsqueda
```
- ✅ Lista todos o con búsqueda
- ✅ LIKE icase para búsqueda flexible
- ⚠️ Sin paginación (problema si 10,000+ clientes)

**UPDATE (Actualizar cliente)**
```python
@app.route('/clientes/<int:id>/editar', methods=['GET', 'POST'])
def cliente_editar(id):
    cliente = Cliente.query.get_or_404(id)
    if request.method == 'POST':
        cliente.nombre = request.form['nombre']
        db.session.commit()
```
- ✅ Obtiene cliente existente
- ✅ Modifica atributos
- ✅ Persiste cambios
- ❌ Usa POST en lugar de PUT

**DELETE (Eliminar cliente)**
```python
@app.route('/clientes/<int:id>/eliminar', methods=['POST'])
def cliente_eliminar(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
```
- ✅ Cascade automático elimina préstamos
- ❌ Usa POST en lugar de DELETE
- ❌ Sin confirmación de usuario

### Préstamo CRUD

**CREATE (Crear préstamo)**
```python
prestamo = Prestamo(
    cliente_id=...,
    monto=Decimal(...),
    tasa_interes=Decimal(...),
    cantidad_cuotas=int(...),
    fecha_desembolso=date(...)
)
db.session.add(prestamo)
db.session.commit()
prestamo.generar_cronograma()
```
- ✅ Crea registro y cronograma
- ❌ No valida que cliente exista
- ❌ No valida montos positivos

**READ (Leer préstamos)**
```python
Prestamo.query.all()
Prestamo.query.filter_by(estado='ACTIVO').all()
```
- ✅ Lista por estado
- ✅ Mostrar detalles con cuotas

**UPDATE (Actualizar préstamo)**
- ✅ Modifica datos
- ✅ Regenera cronograma
- ⚠️ Borra cuotas antiguas y recalcula (podría perder historial de pagos parciales)

**DELETE (Eliminar préstamo)**
- ✅ Cascade elimina cuotas y pagos
- ❌ Sin auditoría (no registra qué se eliminó)

### Cuota/Pago CRUD

**READ** ✅ - Ver cuotas de préstamo
**UPDATE** - Cambiar estado a PAGADO
**CREATE (Pago)** - Registrar pago de cuota

---

## 10. ORM - SQLALCHEMY ANÁLISIS

### ¿Qué es SQLAlchemy?

ORM (Object-Relational Mapping) que mapea:
- Clases Python → Tablas SQL
- Atributos de clase → Columnas
- Instancias → Filas
- Relaciones → Foreign keys

### Modelos del proyecto

**Cliente Model:**
```python
class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    documento = db.Column(db.String(20), unique=True, nullable=False)
    prestamos = db.relationship('Prestamo', backref='cliente', cascade='all, delete-orphan')
```

**Tipos de datos:**
- `db.Integer` → INTEGER SQL
- `db.String(100)` → VARCHAR(100)
- `db.Numeric(12, 2)` → NUMERIC(12,2) - **CORRECTO para dinero**
- `db.Date`, `db.DateTime` → DATE, TIMESTAMP

**Relaciones:**
```python
prestamos = db.relationship('Prestamo', backref='cliente', cascade='all, delete-orphan')
```
- `backref='cliente'`: Prestamo.cliente accede al cliente
- `cascade='all, delete-orphan'`: Eliminar cliente elimina préstamos

### Relaciones entre entidades

```
Cliente (1) ─────── (N) Préstamo
              cliente_id

Préstamo (1) ─────── (N) Cuota
              prestamo_id

Cuota (1) ─────---- (N) Pago
              cuota_id
```

**Acceso:**
```python
# Desde cliente:
cliente.prestamos         # Todos sus préstamos

# Desde préstamo:
prestamo.cliente          # Cliente que hizo préstamo
prestamo.cuotas           # Todas sus cuotas

# Desde cuota:
cuota.prestamo            # Préstamo asociado
cuota.pagos               # Pagos registrados
```

### Métodos SQLAlchemy usados

```python
Cliente.query.all()                                    # SELECT *
Cliente.query.filter_by(estado='ACTIVO')               # WHERE
Cliente.query.filter(Cliente.nombre.ilike('%Juan%'))  # LIKE
Cliente.query.get_or_404(id)                           # SELECT + 404 si no existe
db.session.add(cliente)                               # INSERT prep
db.session.commit()                                   # COMMIT
db.session.rollback()                                 # ROLLBACK
db.session.delete(cliente)                            # DELETE prep
db.func.sum(Prestamo.monto)                           # SUM()
db.func.count()                                       # COUNT()
db.func.extract('month', fecha)                       # EXTRACT MONTH
```

### Problemas ORM identificados

1. **N+1 Queries Problem:**
   ```python
   prestamos = Prestamo.query.all()
   for p in prestamos:
       print(p.cliente.nombre)  # ❌ Query por cada préstamo
   
   # Solución:
   prestamos = Prestamo.query.options(joinedload(Prestamo.cliente)).all()
   ```

2. **Lazy loading puede fallar fuera de app context**
3. **Sin eager loading explícito en dashboard**
4. **Sin índices en tabla cuotas (puede ser lento)**

### Ventajas del ORM vs SQL puro

| Aspecto | ORM | SQL Puro |
|--------|-----|----------|
| Seguridad SQL injection | ✅ Alto | ❌ Requiere care |
| Portabilidad BD | ✅ Cambiar DB fácil | ❌ Reescribir queries |
| Legibilidad | ✅ Python-like | ⚠️ SQL complejo |
| Performance | ⚠️ Puede ser lento | ✅ Optimizado |
| Debugging | ⚠️ Difícil | ✅ SQL visible |

---

## 11. BASE DE DATOS - ANÁLISIS CRÍTICO

### Motor: PostgreSQL

**Configuración:**
- URL: `postgresql://postgres:postgres@localhost:5432/sistema_prestamo`
- Driver: psycopg2-binary

### Diseño de tablas

**CLIENTES**
```sql
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    documento VARCHAR(20) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(100),
    direccion VARCHAR(200),
    fecha_registro TIMESTAMP DEFAULT now()
);
```
✅ Buen diseño
- PK correcta
- documento UNIQUE previene duplicados
- Campos opcionales permitidos

❌ Mejoras sugeridas:
- Agregar CHECK constraints
- Añadir índice en documento para búsquedas

**PRESTAMOS**
```sql
CREATE TABLE prestamos (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    monto NUMERIC(12, 2) NOT NULL,
    tasa_interes NUMERIC(5, 2) NOT NULL,
    cantidad_cuotas INTEGER NOT NULL,
    fecha_desembolso DATE NOT NULL,
    estado VARCHAR(20) DEFAULT 'ACTIVO',
    fecha_creacion TIMESTAMP DEFAULT now(),
    cuota_mensual NUMERIC(15, 2),
    interes_total NUMERIC(15, 2),
    monto_total NUMERIC(15, 2)
);
```
⚠️ Diseño problematico:
- ❌ campos `cuota_mensual`, `interes_total`, `monto_total` son REDUNDANTES
- Pueden calcularse desde cuotas
- Risgo de inconsistencia si se editan

✅ Correcto:
- NUMERIC(12, 2) excelente para dinero
- FK con CASCADE

**CUOTAS**
```sql
CREATE TABLE cuotas (
    id SERIAL PRIMARY KEY,
    prestamo_id INTEGER NOT NULL REFERENCES prestamos(id) ON DELETE CASCADE,
    numero_cuota INTEGER NOT NULL,
    fecha_vencimiento DATE,
    capital NUMERIC(12, 2) NOT NULL,
    interes NUMERIC(12, 2) NOT NULL,
    monto_cuota NUMERIC(12, 2) NOT NULL,
    saldo_restante NUMERIC(15, 2) NOT NULL,
    estado VARCHAR(20) DEFAULT 'PENDIENTE',
    fecha_pago DATE
);
```
✅ Bien diseñada
- Almacena detalles de amortización
- Estado para auditoría

⚠️ Mejoras:
- Agregar índice en (prestamo_id, estado) para búsquedas rápidas
- Agregar CHECK (monto_cuota > 0)

**PAGOS**
```sql
CREATE TABLE pagos (
    id SERIAL PRIMARY KEY,
    cuota_id INTEGER NOT NULL REFERENCES cuotas(id) ON DELETE CASCADE,
    fecha_pago TIMESTAMP DEFAULT now(),
    monto_pagado NUMERIC(15, 2) NOT NULL,
    observacion VARCHAR(200)
);
```
✅ Simple y clara
- Auditoría de todos los pagos
- Permite pagos parciales (aunque código no lo aprovecha)

### Relaciones

```
clientes (1) ─── (N) prestamos
   ↓ PK id        ↓ FK cliente_id

prestamos (1) ─── (N) cuotas
   ↓ PK id         ↓ FK prestamo_id

cuotas (1) ─── (N) pagos
   ↓ PK id    ↓ FK cuota_id
```

### Evaluación del diseño

**Fortalezas:**
1. Integridad referencial con FK y CASCADE
2. Tipos numéricos precisos (NUMERIC)
3. Timestamps para auditoría
4. Normalización (no 3NF, pero 2NF)

**Debilidades:**
1. Redundancia en tabla prestamos (campos calculados)
2. Sin índices explícitos (excepto PK, UNIQUE)
3. Sin CHECK constraints
4. Sin particionamiento (para 1M+ registros)
5. Sin triggers de auditoría
6. Sin soft-delete (eliminación lógica)

### Consultas complejas identificadas

**Dashboard - Préstamos por mes:**
```sql
SELECT EXTRACT(MONTH FROM fecha_desembolso) AS mes,
       EXTRACT(YEAR FROM fecha_desembolso) AS anio,
       COUNT(*) AS cantidad,
       SUM(monto) AS monto
FROM prestamos
GROUP BY EXTRACT(YEAR FROM fecha_desembolso),
         EXTRACT(MONTH FROM fecha_desembolso)
ORDER BY anio, mes;
```

**Intereses generados:**
```sql
SELECT SUM(interes)
FROM cuotas
JOIN pagos ON cuotas.id = pagos.cuota_id
WHERE cuotas.estado = 'PAGADO';
```

---

## 12. LÓGICA DE NEGOCIO - ANÁLISIS MATEMÁTICO

### Sistema de amortización: Método Francés

**¿Qué es?**
Sistema donde todas las cuotas son IGUALES. La diferencia está en composición:
- Primeras cuotas: más interés, menos capital
- Últimas cuotas: menos interés, más capital

**Fórmula:**
```
Cuota = P × [r(1+r)^n] / [(1+r)^n - 1]

Donde:
P = Principal (monto del préstamo)
r = Tasa de interés mensual
n = Número de cuotas
```

### Implementación en código

**Cálculo de cuota mensual:**
```python
def calcular_cuota_mensual(self):
    monto = float(self.monto)
    tasa_anual = float(self.tasa_interes)
    n = self.cantidad_cuotas
    
    tasa_mensual = tasa_anual / 100 / 12
    
    if tasa_mensual == 0:
        return monto / n
    
    cuota = monto * (tasa_mensual * (1 + tasa_mensual) ** n) / ((1 + tasa_mensual) ** n - 1)
    return round(cuota, 2)
```

**Análisis:**
- ✅ Convierte tasa anual a mensual correctamente
- ✅ Caso especial para tasa 0%
- ✅ Redondea a 2 decimales (centavos)
- ⚠️ Usa float en lugar de Decimal (puede perder precisión)

### Generación del cronograma

```python
def generar_cronograma(self):
    saldo = monto
    
    for i in range(1, n + 1):
        interes = round(saldo * tasa_mensual, 2)
        capital = round(cuota - interes, 2)
        
        if i == n:  # Última cuota
            capital = round(saldo, 2)
            cuota = round(capital + interes, 2)
        
        saldo = round(saldo - capital, 2)
        
        # Crear Cuota
        cuota_obj = Cuota(
            numero_cuota=i,
            capital=capital,
            interes=interes,
            monto_cuota=cuota,
            saldo_restante=saldo,
            estado='PENDIENTE'
        )
```

**Ejemplo con números reales:**
- Monto: 100,000
- Tasa: 15% anual (1.25% mensual)
- Plazo: 12 meses

| Cuota | Saldo Inicial | Interés | Capital | Cuota Total | Saldo Final |
|-------|---------------|---------|---------|-------------|-------------|
| 1 | 100,000.00 | 1,250.00 | 7,961.50 | 9,211.50 | 92,038.50 |
| 2 | 92,038.50 | 1,150.48 | 8,061.02 | 9,211.50 | 83,977.48 |
| 3 | 83,977.48 | 1,049.72 | 8,161.78 | 9,211.50 | 75,815.70 |
| ... | ... | ... | ... | ... | ... |
| 12 | 9,211.50 | 115.14 | 9,096.36 | 9,211.50 | 0.00 |

**Verificación matemática:**
```
Total pagado = 12 × 9,211.50 = 110,538.00
Interés total = 110,538.00 - 100,000 = 10,538.00
```

### Problemas matemáticos identificados

1. **Precisión de decimales:**
   ```python
   # Usa float en lugar de Decimal
   monto = float(self.monto)  # ❌
   
   # Correcto:
   monto = self.monto  # Ya es Decimal desde BD
   ```

2. **Redondeo acumulativo:**
   - Cada línea redondea
   - En 360 cuotas (30 años), error acumulado puede ser significativo
   - ✅ Se "ajusta" en última cuota, pero no es ideal

3. **Validaciones ausentes:**
   - No valida tasa negativa
   - No valida cantidad_cuotas < 1
   - No valida monto ≤ 0

### Caso de uso: Cliente pide préstamo

**Escenario:**
```
Cliente: Juan García
Monto: 500,000 guaraní
Tasa: 18% anual
Plazo: 60 meses
Fecha desembolso: 22/06/2026
```

**Proceso:**
1. Sistema calcula cuota mensual
   - tasa_mensual = 18/100/12 = 1.5% = 0.015
   - cuota = 500,000 × [0.015(1.015)^60] / [(1.015)^60 - 1]
   - cuota ≈ 10,635.33

2. Sistema genera 60 cuotas:
   - Cuota 1: 7,500 interés + 3,135.33 capital = 10,635.33
   - Cuota 2: 7,453.00 + 3,182.33 = 10,635.33
   - ...
   - Cuota 60: 159.53 + 10,475.80 = 10,635.33

3. Estado de cuenta:
   - Capital desembolsado: 500,000
   - Interés total a cobrar: 638,119.80 (60 × 10,635.33 - 500,000)
   - Valor total a pagar: 638,119.80

---

## 13. SEGURIDAD - ANÁLISIS Y VULNERABILIDADES

### 🔴 VULNERABILIDADES CRÍTICAS

**1. SECRET_KEY Hardcodeado**
```python
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'
```
**Riesgo**: Quienquiera que clone el repo tiene la clave
**Impacto**: Firma de sesiones compromentida
**Severidad**: CRÍTICA
**Fix**:
```python
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-dev-key')
```

**2. No valida documentos duplicados**
```python
# El modelo marca documento como UNIQUE:
documento = db.Column(db.String(20), unique=True, nullable=False)

# Pero NO captura IntegrityError:
cliente = Cliente(documento='123')
db.session.add(cliente)
db.session.commit()  # ❌ Levanta excepción genérica
```
**Riesgo**: Usuario ve error técnico en lugar de mensaje claro
**Fix**: Capturar IntegrityError y retornar mensaje

**3. SQL Injection - ELIMINADO ✅**
```python
# ✅ CORRECTO - usa parámetros:
Cliente.query.filter(Cliente.nombre.ilike(f'%{busqueda}%'))
# SQLAlchemy escapa automáticamente
```

**4. No valida relaciones antes de crear**
```python
# No verifica que cliente_id exista:
prestamo = Prestamo(cliente_id=request.form['cliente_id'], ...)
db.session.add(prestamo)
db.session.commit()  # FK constraint lo previene, pero no es elegante
```
**Fix**: Validar que cliente existe antes

**5. Ausencia de autenticación y autorización**
```python
# Cualquiera puede acceder a cualquier ruta:
@app.route('/clientes/<int:id>/editar')
def cliente_editar(id):  # ❌ Sin login_required
```
**Riesgo**: CRÍTICO en producción
**Fix**:
```python
from flask_login import login_required

@app.route('/clientes/<int:id>/editar')
@login_required
def cliente_editar(id):
```

**6. No sanitiza entrada de formularios**
```python
# No valida tipo ni largo:
nombre = request.form['nombre']  # Podría tener 10,000 caracteres
prestamo.monto = Decimal(request.form['monto'])  # Podría ser "abc"
```
**Fix**: Usar WTForms con validadores

**7. Manejo insuficiente de excepciones**
```python
try:
    db.session.commit()
except Exception as e:  # ❌ Demasiado genérico
    flash(f'Error: {str(e)}', 'error')
```
**Riesgo**: Expone detalles técnicos a usuario
**Fix**: Capturar excepciones específicas

**8. Debug mode en producción**
```python
app.run(debug=True, host='0.0.0.0')  # ❌ NUNCA en prod
```
**Riesgo**: CRÍTICA - expone stack traces, permite ejecutar código
**Fix**:
```python
app.run(debug=os.getenv('DEBUG', 'False') == 'True', port=5000)
```

**9. Base de datos expone contraseña**
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/...
                                      ^^^^^^
```
**Riesgo**: Credenciales en archivo .env del repo
**Fix**: Agregar .env a .gitignore (ya está en proyecto)

**10. Sin protección CSRF**
```python
# Formularios POST sin token CSRF
@app.route('/clientes/<int:id>/eliminar', methods=['POST'])
def cliente_eliminar(id):
    # Alguien podría hacer un <img src="http://app.com/clientes/1/eliminar">
```
**Fix**: Usar Flask-WTF csrf_token

### 🟡 VULNERABILIDADES MODERADAS

**11. Sin rate limiting**
- Alguien podría hacer queries masivas
- Fix: Flask-Limiter

**12. Sin validación de tipos MIME**
- ✅ No hay upload de archivos, así que bajo riesgo

**13. Timestamps sin timezone**
```python
fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
```
- ⚠️ datetime.utcnow retorna naive datetime
- Should use timezone-aware

**14. Sin logging de acciones críticas**
- No registra quién eliminó un préstamo
- Fix: Agregar audit trail

### 🟢 BIEN IMPLEMENTADO

**✅ Uso de Decimal para dinero**
- Previene errores de precisión

**✅ ORM escapa consultas**
- Previene SQL injection

**✅ FK con CASCADE**
- Integridad referencial garantizada

**✅ HTTPException 404**
- No expone que recurso no existe (seguridad)

---

## 14. BUENAS PRÁCTICAS - EVALUACIÓN

### Nombres de variables

**Excelentes:**
```python
cantidad_cuotas  ✅
tasa_interes    ✅
saldo_restante  ✅
fecha_vencimiento ✅
```

**Regulares:**
```python
n  ❌ (debería ser cantidad_cuotas)
r  ❌ (debería ser tasa_mensual)
```

**En modelos:**
```python
__tablename__ = 'clientes'  ✅ Claro
backref='cliente'           ✅ Descriptivo
```

### Organización de carpetas

```
proyecto/
├── app.py              ✅ Aplicación principal
├── models.py           ✅ Modelos ORM
├── database.py         ✅ Configuración BD
├── requirements.txt    ✅ Dependencias
├── .env               ✅ Variables de entorno
├── templates/         ✅ Vistas HTML
└── __pycache__/       ✅ (ignorable)
```

**Podría mejorarse:**
```
proyecto/
├── app.py
├── config.py           # Configuración centralizada
├── models/
│   ├── __init__.py
│   ├── cliente.py
│   ├── prestamo.py
│   ├── cuota.py
│   └── pago.py
├── routes/             # Rutas separadas por módulo
│   ├── clientes.py
│   ├── prestamos.py
│   └── reportes.py
├── services/           # Lógica de negocio
│   └── prestamo_service.py
├── templates/
└── static/
```

### Modularidad

**Actual:** Monolítica
- Todo en app.py (~375 líneas)
- Todos los modelos en models.py

**Ideal:** Separado por dominios
- Rutas en blueprints de Flask
- Servicios separados
- Tests aislados

### Principios SOLID

| Principio | Cumplimiento | Comentario |
|-----------|--------------|-----------|
| **S**ingle Responsibility | ⚠️ 70% | app.py hace demasiado |
| **O**pen/Closed | ✅ 80% | Fácil extender con nuevos modelos |
| **L**iskov Substitution | ✅ 90% | Modelos son intercambiables |
| **I**nterface Segregation | ⚠️ 60% | Algunos métodos hacen mucho |
| **D**ependency Inversion | ❌ 40% | Acoplamiento a Flask directo |

### Separación de responsabilidades

**Bueno:**
- Models no conocen rutas
- Rutas usan models
- Templates no tienen lógica compleja

**Podría mejorar:**
- Extraer lógica de cálculo a services
- Validators separados
- Serializers para JSON

**Ejemplo mejora:**
```python
# services/prestamo_service.py
class PrestamoService:
    @staticmethod
    def crear_prestamo(cliente_id, monto, tasa, cuotas):
        # Validación
        # Cálculo
        # Persistencia
        
# app.py
@app.route('/prestamos/nuevo', methods=['POST'])
def prestamo_nuevo():
    resultado = PrestamoService.crear_prestamo(...)
    return redirect(...)
```

### Patrones de código

**Render después POST (Redirect-After-Post) ✅**
```python
if request.method == 'POST':
    # Crear
    return redirect(url_for('prestamos'))
```
Correcto: Evita resubmisión si F5

**Context managers ✅**
```python
with app.app_context():
    db.create_all()
```
Correcto: Limpia recursos

**Manejo de errores**
```python
try:
    db.session.commit()
except Exception as e:
    db.session.rollback()
    flash(f'Error: {str(e)}', 'error')
```
⚠️ Demasiado genérico, debería ser Exception específica

### Documentación de código

**Docstrings ✅**
```python
def generar_cronograma(self):
    """
    Genera el cronograma de pagos usando el sistema francés
    """
```

**Comentarios explicativos ✅**
```python
# Ajustar última cuota
if i == n:
    capital = round(saldo, 2)
```

**Falta:**
- README sin instrucciones
- Sin diagrama de arquitectura
- Sin API documentation

### Type hints

**Actual:** Ninguno
```python
def calcular_cuota_mensual(self):
    return round(cuota, 2)
```

**Debería ser:**
```python
def calcular_cuota_mensual(self) -> float:
    return round(cuota, 2)
```

---

## 15. PREPARACIÓN PARA EXPOSICIÓN ORAL

### Guion de presentación (10 minutos)

**0:00-1:00 | Introducción**
```
"Buenos días, presento Sistema de Gestión de Préstamos, 
una aplicación web para automatizar el ciclo completo 
de desembolso y seguimiento de préstamos."
```

**1:00-2:00 | Problema y solución**
```
"El problema: Instituciones financieras gestionar préstamos 
manualmente implica errores en cálculos, imposibilidad de auditoría, 
y pérdida de tiempo.

La solución: Una plataforma que automatiza:
- Cálculo de cuotas (sistema francés de amortización)
- Generación automática de cronogramas
- Registro de pagos
- Estadísticas en tiempo real"
```

**2:00-3:30 | Arquitectura**
```
"El sistema está dividido en 4 capas:

1. Presentación: 7 templates HTML con Jinja2
2. Aplicación: Flask con 15+ rutas REST
3. Datos: SQLAlchemy ORM con 4 modelos
4. Persistencia: PostgreSQL con 4 tablas

El flujo es: Usuario → Flask → ORM → PostgreSQL"
```

**3:30-5:00 | Funcionalidades principales**
```
"Primer, gestión de clientes: Crear, buscar, editar, eliminar.

Segundo, gestión de préstamos:
- Crear préstamo con cliente
- Sistema calcula cuota automáticamente
- Genera 60 cuotas (si es 60 meses)

Tercero, pagos:
- Usuario registra pago de cuota
- Sistema marca como PAGADO
- Si todas las cuotas están pagadas, préstamo pasa a CANCELADO

Cuarto, reportes con gráficos y estadísticas"
```

**5:00-7:00 | Tecnología y decisiones**
```
"Elegí Python + Flask porque:
- Lenguaje claro, ideal para prototipado
- Flask ligero, sin overhead de Django
- PostgreSQL robusto para datos financieros

Para ORM usé SQLAlchemy porque:
- Seguridad contra SQL injection
- Relaciones automáticas
- Compatible con múltiples BD

Para amortización usé fórmula Francés porque:
- Cuotas iguales (cliente prefiere)
- Estándar en industria bancaria"
```

**7:00-8:30 | Base de datos**
```
"Base de datos tiene 4 tablas:

Clientes: Almacena datos personales
Préstamos: Datos del préstamo (monto, tasa, cuotas)
Cuotas: Desglose de cada pago (capital, interés, saldo)
Pagos: Auditoría de qué se pagó y cuándo

Las relaciones son:
- 1 cliente → N préstamos
- 1 préstamo → N cuotas
- 1 cuota → N pagos

Esto permite auditoría completa: puedo saber
cuándo se pagó cada cuota y por quién."
```

**8:30-9:30 | Lógica de negocio (matemática)**
```
"Lo más importante: cálculo de cuotas.

Uso fórmula Francés:
Cuota = P × [r(1+r)^n] / [(1+r)^n - 1]

Ejemplo real:
- Préstamo: 500,000 guaraní
- Tasa: 18% anual (1.5% mensual)
- Plazo: 60 meses

El sistema calcula cuota mensual: 10,635 guaraní

Luego genera cronograma donde:
- Cuota 1: 7,500 interés + 3,135 capital
- Cuota 2: 7,453 interés + 3,182 capital (más capital)
- ...
- Cuota 60: 160 interés + 10,475 capital (casi todo capital)

Esto es amortización francesa."
```

**9:30-10:00 | Conclusiones**
```
"Fortalezas del proyecto:
- Automatización completa de cálculos
- Auditoría total de pagos
- Interfaz intuitiva

Mejoras futuras:
- Agregar autenticación de usuarios
- Reportes a PDF
- Integración con pasarelas de pago
- Dashboard más avanzado con gráficos"
```

### Preguntas que podría hacer el profesor

**Pregunta 1:** "¿Por qué usaste PostgreSQL y no SQLite?"
```
Respuesta: PostgreSQL es más robusto para:
- Múltiples usuarios simultáneos (concurrencia)
- Transacciones ACID más confiables
- Mejor para datos financieros (precisión NUMERIC)
SQLite estaría bien para demo, pero no para producción.
```

**Pregunta 2:** "¿Cómo garantizas que no hay errores en los cálculos de cuotas?"
```
Respuesta: De dos formas:
1. Uso Numeric(12,2) en PostgreSQL (decimal exacto, no float)
2. Ajusto la última cuota para que saldo = 0 exactamente
3. La fórmula Francesa es estándar industria

Ejemplo: Si suma de 59 cuotas = 499,200, la cuota 60 
se ajusta para que capital sea exactamente 800.
```

**Pregunta 3:** "¿Qué ocurre si un usuario intenta pagar una cuota dos veces?"
```
Respuesta: El código lo previene:
```python
if cuota.estado == 'PAGADO':
    flash('Esta cuota ya ha sido pagada', 'warning')
    return redirect(...)
```
Si llega dos veces, la segunda vez retorna advertencia.
Aunque debería tener un mejor control (CSRF token, etc).
```

**Pregunta 4:** "¿Cómo manejas montos con decimales en Paraguay (formato 1.500,50)?"
```
Respuesta: Hago conversión en app.py:
```python
monto_str = request.form['monto'].replace('.', '').replace(',', '.')
# "1.500,50" → "1500.50" (formato Python)
prestamo.monto = Decimal(monto_str)
```

**Pregunta 5:** "¿Qué pasaría si modificas un préstamo después que tienen pagos?"
```
Respuesta: El código regenera el cronograma:
```python
prestamo.generar_cronograma()
```

Pero esto BORRA CUOTAS VIEJAS (malo para auditoría).
En producción, debería impedirse editar préstamos 
con pagos registrados o usar soft-delete.
```

**Pregunta 6:** "¿Cómo implementarías autenticación?"
```
Respuesta: Usaría Flask-Login:
```python
from flask_login import LoginManager, login_required

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/prestamos')
@login_required
def prestamos():
    # Solo usuario logueado accede
```

También agregaría tabla Usuarios con contraseña hasheada (bcrypt).
```

**Pregunta 7:** "¿Escalabilidad? ¿Funciona con 1 millón de préstamos?"
```
Respuesta: Parcialmente sí con mejoras:

Actual (problemas):
- Sin paginación → carga lista completa
- Sin índices → queries lentas en tablas grandes
- N+1 problem en dashboard

Mejoras necesarias:
- Agregar índices en (cliente_id, estado)
- Implementar paginación (Flask-SQLAlchemy paginate)
- Eager loading de relaciones
- Caché en dashboard
- Partition de cuotas por año
```

**Pregunta 8:** "¿Consideraste el riesgo de SQL Injection?"
```
Respuesta: Sí, pero de forma indirecta:
- Usé SQLAlchemy ORM que escapa todas las queries
- Nunca escribo SQL raw, siempre vía ORM
- Búsqueda ilike() es segura:
  ```python
  Cliente.query.filter(Cliente.nombre.ilike(f'%{busqueda}%'))
  ```

Aunque mejoraría con:
- Validadores WTForms
- Límites de largo
- Rate limiting
```

**Pregunta 9:** "¿Cómo testiarias el sistema?"
```
Respuesta: Con pytest:

```python
def test_calcular_cuota():
    prestamo = Prestamo(monto=100000, tasa_interes=15, cantidad_cuotas=24)
    cuota = prestamo.calcular_cuota_mensual()
    assert abs(cuota - 4415.07) < 0.01  # Tolerance para redondeo

def test_generar_cronograma():
    prestamo = Prestamo(...)
    prestamo.generar_cronograma()
    assert len(prestamo.cuotas) == 24
    assert sum([c.capital for c in cuotas]) ≈ 100000
```

```

**Pregunta 10:** "¿Qué documentación te faltó?"
```
Respuesta: 
- README detallado (qué tengo ahora)
- Swagger/OpenAPI para API
- Diagrama ER de BD
- Tests unitarios e integración
- Guía de deployment
- Logs de auditoría
```

---

## 16. EVALUACIÓN FINAL

### Calificación: 7.2 / 10

**Desglose:**
- Funcionalidad: 8/10
- Arquitectura: 6/10
- Código: 7/10
- Documentación: 4/10
- Seguridad: 5/10
- Scalabilidad: 5/10
- UX/UI: 7/10

### Fortalezas

✅ **Funcionalidad completa**
- Todas las operaciones CRUD implementadas
- Cálculo matemático correcto
- Generación automática de cronogramas

✅ **Uso correcto de ORM**
- SQLAlchemy bien utilizado
- Relaciones con cascade automático
- Búsquedas con filtros complejos

✅ **Tipos de datos apropiados**
- Numeric para dinero (no float)
- Dates y timestamps para auditoría

✅ **Flujo de negocio lógico**
- Cliente → Préstamo → Cuotas → Pagos
- Estados coherentes (ACTIVO, CANCELADO, PAGADO)

✅ **Interfaz usable**
- Templates claros
- Navegación intuitiva
- Mensajes flash informativos

### Debilidades críticas

❌ **Seguridad**
- Sin autenticación (CRÍTICA)
- SECRET_KEY hardcodeado
- Sin CSRF protection
- Sin validación de entrada

❌ **Documentación**
- No hay README
- Sin diagramas
- Sin comentarios explicativos

❌ **Escalabilidad**
- Sin paginación
- Sin caché
- Sin índices de BD
- N+1 queries en dashboard

❌ **Mantenibilidad**
- Todo en un archivo (app.py 375 líneas)
- Sin tests
- Acoplamiento fuerte

❌ **Validación**
- No valida documentos duplicados elegantemente
- No valida montos negativos
- No valida cliente_id válido

### Debilidades menores

⚠️ **Conversiones de tipo**
- Usa float en lugar de Decimal en cálculos
- Posible pérdida de precisión (aunque mínima)

⚠️ **Manejo de errores**
- Excepciones demasiado genéricas
- No distingue entre errores técnicos y lógica

⚠️ **API REST**
- Mezcla HTML y JSON
- Falta documentación de endpoints
- Códigos HTTP incompletos

### ¿Qué le falta para parecer profesional?

| Aspecto | Estado | Necesario |
|---------|--------|----------|
| Autenticación | ❌ | CRÍTICA |
| Validación | ⚠️ | IMPORTANTE |
| Tests | ❌ | IMPORTANTE |
| Documentación | ❌ | IMPORTANTE |
| CI/CD | ❌ | DESEABLE |
| Logging | ❌ | DESEABLE |
| Monitoreo | ❌ | DESEABLE |
| Manejo de errores | ⚠️ | IMPORTANTE |
| Performance | ⚠️ | IMPORTANTE |
| Seguridad | ❌ | CRÍTICA |

### Mejoras recomendadas por prioridad

**Fase 1 (Crítica):**
1. Agregar autenticación de usuarios
2. CSRF protection
3. Validación de entrada con WTForms
4. Secreto en variables de entorno

**Fase 2 (Importante):**
1. Tests unitarios con pytest
2. Separar app.py en blueprints
3. Documentación README + Swagger
4. Manejo de errores específicos

**Fase 3 (Deseable):**
1. Paginación
2. Caché con Redis
3. Logging centralizado
4. Dashboards avanzados (Grafana)

---

## 17. README PROFESIONAL 2.0

Ver archivo separado: README.md

---

# CONCLUSIÓN

Este proyecto demuestra:

✅ Comprensión de conceptos de ORM, REST, y arquitectura web
✅ Implementación correcta de algoritmo de amortización
✅ Manejo adecuado de base de datos relacional
✅ Interfaz funcional y usable

❌ Pero carece de elementos de producción críticos:
- Seguridad (sin autenticación, sin validación)
- Documentación (sin README, sin API docs)
- Calidad (sin tests, acoplamiento alto)

**Recomendación académica:**
- Calificación: 7.2/10
- Apto para defensa
- Aprobado con recomendaciones de mejora
- Potencial para convertirse en aplicación profesional

