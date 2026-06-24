# 📊 Sistema de Gestión de Préstamos - README 2.0

**Última actualización:** Junio 2026 | **Versión:** 1.0.0 | **Estado:** En Producción

---

## 📋 Tabla de Contenidos

1. [Descripción](#descripción)
2. [Objetivos](#objetivos)
3. [Características](#características)
4. [Arquitectura](#arquitectura)
5. [Tecnologías](#tecnologías)
6. [Instalación](#instalación)
7. [Uso](#uso)
8. [API Endpoints](#api-endpoints)
9. [Base de Datos](#base-de-datos)
10. [Guía de Administración](#guía-de-administración)
11. [Mejoras Futuras](#mejoras-futuras)
12. [Licencia](#licencia)

---

## Descripción

**Sistema de Gestión de Préstamos** es una aplicación web integrada diseñada para instituciones financieras, cooperativas de crédito y entidades de microfinanzas que necesiten automatizar el ciclo completo de gestión de préstamos.

El sistema automatiza:
- ✅ Registro de clientes
- ✅ Solicitud y desembolso de préstamos
- ✅ **Cálculo automático de cuotas** (Sistema Francés de Amortización)
- ✅ Generación de cronogramas de pago
- ✅ Registro de pagos realizados
- ✅ Auditoría completa de transacciones
- ✅ Reportes y estadísticas en tiempo real

### ¿Para quién es este sistema?

- Cooperativas de crédito
- Instituciones de microfinanzas
- Empresas de factoring
- Fondos de empleados
- Prestamistas formales que necesitan profesionalizar su operación

---

## Objetivos

### Objetivo General
Proporcionar una plataforma automatizada que garantice precisión en cálculos de préstamos, auditoría completa de operaciones y facilite la toma de decisiones con reportes en tiempo real.

### Objetivos Específicos

1. **Precisión Matemática**: Garantizar cálculos exactos usando fórmula Francesa de amortización
2. **Auditoría Completa**: Registrar cada transacción con trazabilidad total
3. **Eficiencia Operativa**: Reducir tiempo de procesamiento de prestamos de horas a segundos
4. **Escalabilidad**: Soportar desde 100 hasta 100,000+ operaciones sin degradación
5. **Usabilidad**: Interfaz intuitiva que no requiera capacitación técnica
6. **Integrabilidad**: API REST para conectar con otros sistemas

---

## Características

### 1. Gestión de Clientes 👥

```
✅ CRUD completo de clientes
✅ Búsqueda avanzada por nombre, apellido, documento
✅ Validación de documentos únicos
✅ Almacenamiento de contacto (teléfono, email)
✅ Historial de préstamos por cliente
```

**Ejemplo:**
```
Cliente: Juan García López
Documento: 3.456.789-1
Teléfono: +595 (9) 87 654321
Correo: juan.garcia@example.com
Dirección: Calle Principal 123, Asunción
Préstamos activos: 2
Préstamos cancelados: 1
```

### 2. Gestión de Préstamos 💰

```
✅ Crear préstamos con datos completos
✅ Asignar cliente automáticamente
✅ Ingresar monto, tasa y plazo
✅ Cálculo automático de cuota mensual
✅ Generación automática de cronograma
✅ Visualizar todos los préstamos
✅ Editar datos (regenera cronograma)
✅ Filtrar por estado (ACTIVO/CANCELADO)
```

**Parámetros de crédfito:**
- Monto: Flexible (desde 100,000 a 1,000,000,000 guaraní)
- Tasa de interés: 0% a 30% anual
- Plazo: 1 a 360 meses
- Fecha de desembolso: Configurable

### 3. Cálculo Automático de Cuotas 🧮

**Sistema Francés de Amortización**

Todas las cuotas son de igual monto. La diferencia está en la composición:
- Cuotas iniciales: Más interés, menos capital
- Cuotas finales: Menos interés, más capital

```
Ejemplo: Préstamo de 500,000 al 18% en 60 cuotas

Cuota calculada: 10,635.33 guaraní
Interés total: 138,119.80 guaraní
Monto total a pagar: 638,119.80 guaraní

Mes 1:  Interés 7,500 + Capital 3,135.33 = 10,635.33
Mes 2:  Interés 7,453 + Capital 3,182.33 = 10,635.33
...
Mes 60: Interés 160 + Capital 10,475.33 = 10,635.33
```

### 4. Cronograma de Pagos 📅

```
✅ Generación automática (hasta 360 cuotas)
✅ Detalles: Capital, Interés, Saldo Restante
✅ Fecha de vencimiento de cada cuota
✅ Estado de cada cuota (PENDIENTE/PAGADO)
✅ Visualización completa del cronograma
```

### 5. Registro de Pagos 💳

```
✅ Marcar cuota como pagada
✅ Registrar fecha de pago
✅ Observaciones (cheque número, referencia, etc.)
✅ Cambio automático de estado del préstamo
✅ Auditoría completa de pagos
```

### 6. Dashboard y Reportes 📊

**Estadísticas en tiempo real:**
```
- Total clientes registrados
- Total préstamos creados
- Préstamos activos vs cancelados
- Capital total desembolsado
- Intereses generados (acumulado)
- Gráficos de tendencia por mes
```

**Reportes disponibles:**
```
- Reporte de todos los préstamos
- Consultas filtradas (por cliente, estado)
- Exportable a datos (para análisis)
```

---

## Arquitectura

### Diseño de capas

```
┌──────────────────────────────────────────┐
│     PRESENTACIÓN (Templates HTML)         │
│  dashboard.html, clientes.html, etc.      │
└────────────────────┬─────────────────────┘
                     │ HTTP/JSON
                     │
┌─────────────────────────────────────────┐
│  APLICACIÓN (Flask Application)          │
│  ├─ 15+ Rutas (GET/POST)                 │
│  ├─ Lógica de negocio                    │
│  └─ Manejo de requests/responses          │
└────────────────────┬────────────────────┘
                     │ SQLAlchemy ORM
                     │
┌─────────────────────────────────────────┐
│   DATOS (Modelos ORM)                    │
│  ├─ Cliente                              │
│  ├─ Préstamo                             │
│  ├─ Cuota                                │
│  └─ Pago                                 │
└────────────────────┬────────────────────┘
                     │ PostgreSQL Driver
                     │
┌─────────────────────────────────────────┐
│   PERSISTENCIA (PostgreSQL)              │
│  ├─ clientes                             │
│  ├─ prestamos                            │
│  ├─ cuotas                               │
│  └─ pagos                                │
└─────────────────────────────────────────┘
```

### Flujo de datos típico

```
1. Usuario ingresa /prestamos/nuevo
   ↓
2. Flask renderiza form con clientes
   ↓
3. Usuario completa datos y envía POST
   ↓
4. Flask valida y crea Prestamo
   ↓
5. SQLAlchemy convierte a SQL INSERT
   ↓
6. PostgreSQL persiste en tabla prestamos
   ↓
7. Flask ejecuta generar_cronograma()
   ↓
8. Para cada cuota, INSERT en tabla cuotas
   ↓
9. Redirect a /prestamos
   ↓
10. Usuario ve lista actualizada con nuevo préstamo
```

---

## Tecnologías

### Stack principal

| Capa | Tecnología | Versión | Rol |
|------|-----------|---------|-----|
| **Framework** | Flask | 3.0.0 | Web framework |
| **ORM** | Flask-SQLAlchemy | 3.1.1 | Mapeo objeto-relacional |
| **BD** | PostgreSQL | 12+ | Base de datos |
| **Driver BD** | psycopg2 | 2.9.0+ | Conexión a PostgreSQL |
| **Config** | python-dotenv | 1.0.0 | Variables de entorno |
| **Templating** | Jinja2 | (incluido) | Renderizado HTML |

### Por qué estas tecnologías

**Flask vs Django:**
- Flask: Más ligero, control total, curva aprendizaje suave
- Django: Más pesado, incluye admin, ORM nativo

**PostgreSQL vs MySQL vs SQLite:**
- PostgreSQL: Mejor concurrencia, tipos precisos (NUMERIC), ACID
- MySQL: Más ligero pero menos confiable para transacciones críticas
- SQLite: Solo local, no para múltiples usuarios

**SQLAlchemy:**
- Seguridad contra SQL injection
- Relaciones automáticas
- Migraciones posibles

---

## Instalación

### Requisitos previos

```bash
✅ Python 3.8+
✅ PostgreSQL 12+
✅ pip (gestor de paquetes Python)
✅ Git (control de versiones)
```

### Paso 1: Clonar repositorio

```bash
git clone https://github.com/tuusuario/sistema-prestamos.git
cd sistema-prestamos
```

### Paso 2: Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

Esto instala:
- **Flask 3.0.0**: Framework web
- **Flask-SQLAlchemy 3.1.1**: ORM
- **psycopg2-binary**: Driver PostgreSQL
- **python-dotenv**: Cargar .env

### Paso 4: Configurar base de datos

**Crear base de datos en PostgreSQL:**

```sql
-- Conectarse a PostgreSQL
psql -U postgres

-- Crear base de datos
CREATE DATABASE sistema_prestamo;
CREATE USER prestamo_user WITH PASSWORD 'contraseña_segura';
ALTER ROLE prestamo_user SET client_encoding TO 'utf8';
ALTER ROLE prestamo_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE prestamo_user SET default_transaction_deferrable TO on;
GRANT ALL PRIVILEGES ON DATABASE sistema_prestamo TO prestamo_user;
```

**Crear archivo .env:**

```bash
cat > .env << EOF
DATABASE_URL=postgresql://prestamo_user:contraseña_segura@localhost:5432/sistema_prestamo
FLASK_ENV=development
DEBUG=True
SECRET_KEY=tu-clave-secreta-aqui-cambia-en-produccion
EOF
```

**Opciones de DATABASE_URL:**

```
# Local
postgresql://usuario:contraseña@localhost:5432/sistema_prestamo

# En servidor remoto
postgresql://usuario:contraseña@192.168.1.100:5432/sistema_prestamo

# Con RDS (Amazon)
postgresql://usuario:contraseña@db.amazonaws.com:5432/sistema_prestamo
```

### Paso 5: Inicializar base de datos

```bash
# Crear todas las tablas
python reset_db.py

# Output esperado:
# Tablas eliminadas exitosamente
# Tablas creadas exitosamente
```

### Paso 6: Ejecutar aplicación

```bash
python app.py

# Output:
#  * Serving Flask app 'app'
#  * Running on http://0.0.0.0:5000
#  * Debug mode: on
```

**Acceder:** http://localhost:5000

---

## Uso

### Flujo básico de usuario

#### 1. Registrar nuevo cliente

```
HOME → Clientes → Nuevo Cliente

Ingresar:
- Nombre: Juan
- Apellido: Pérez
- Documento: 3456789
- Teléfono: +595987654321
- Email: juan@example.com
- Dirección: Calle Principal 123

Guardar → Se crea cliente
```

#### 2. Crear préstamo

```
HOME → Préstamos → Nuevo Préstamo

Seleccionar cliente: Juan Pérez
Ingresar monto: 500.000 (formato: 500.000)
Ingresar tasa: 18 (porcentaje anual)
Ingresar plazo: 60 (meses)
Fecha desembolso: 22/06/2026

Guardar → Sistema calcula cuota automáticamente
```

**Resultado automático:**
```
Cuota mensual: 10,635.33
Interés total: 138,119.80
Monto total a pagar: 638,119.80
Cronograma de 60 cuotas generado
```

#### 3. Ver cronograma

```
HOME → Préstamos → [Seleccionar préstamo]

Ver detalles:
- Cuota 1: 22/07/2026 - Interés 7,500 + Capital 3,135.33 = 10,635.33
- Cuota 2: 22/08/2026 - Interés 7,453 + Capital 3,182.33 = 10,635.33
...
- Cuota 60: 21/04/2031 - Interés 160 + Capital 10,475.33 = 10,635.33

Botón "Pagar" en cada cuota
```

#### 4. Registrar pago

```
Cronograma → [Cuota 1] → Pagar

Sistema registra:
- Fecha pago: 22/07/2026
- Monto: 10,635.33
- Estado: PAGADO

Cuota pasa a color verde ✓
```

#### 5. Ver reportes

```
HOME → Reportes

Ver:
- Total clientes: 45
- Total préstamos: 128
- Préstamos activos: 115
- Capital desembolsado: 2,350,000
- Intereses generados: 425,000
- Gráfico de préstamos por mes
```

---

## API Endpoints

### Endpoints disponibles

#### 1. Dashboard
```
GET /
Retorna: Página principal con estadísticas
Acceso: Público
```

#### 2. Clientes

```
GET /clientes
Retorna: Lista de todos los clientes
Parámetros: ?busqueda=Juan (opcional)
Ejemplo: /clientes?busqueda=García

GET /clientes/nuevo
Retorna: Formulario para crear cliente
Método: GET para formulario, POST para guardar

POST /clientes/nuevo
Datos requeridos:
{
  "nombre": "Juan",
  "apellido": "Pérez",
  "documento": "3456789",
  "telefono": "+595987654321",
  "correo": "juan@example.com",
  "direccion": "Calle Principal 123"
}
Retorna: Redirect a /clientes

GET /clientes/<id>/editar
Retorna: Formulario prellenado para editar

POST /clientes/<id>/editar
Datos: Igual a crear
Retorna: Redirect a /clientes

POST /clientes/<id>/eliminar
Parámetros: id en URL
Retorna: Redirect a /clientes
Nota: Elimina cliente y todos sus préstamos
```

#### 3. Préstamos

```
GET /prestamos
Retorna: Lista de todos los préstamos
Parámetros: ?estado=ACTIVO (opcional)
Opciones: ACTIVO, CANCELADO

GET /prestamos/nuevo
Retorna: Formulario para crear préstamo

POST /prestamos/nuevo
Datos requeridos:
{
  "cliente_id": 1,
  "monto": "500.000",
  "tasa_interes": "18.50",
  "cantidad_cuotas": "60",
  "fecha_desembolso": "2026-06-22",
  "estado": "ACTIVO"
}
Retorna: Redirect a /prestamos
Nota: Genera cronograma automáticamente

GET /prestamos/<id>
Retorna: Detalle + cronograma completo
Ejemplo: /prestamos/1

GET /prestamos/<id>/editar
Retorna: Formulario prellenado

POST /prestamos/<id>/editar
Datos: Igual a crear
Nota: Regenera cronograma

POST /prestamos/<id>/eliminar
Retorna: Redirect a /prestamos
```

#### 4. Pagos

```
POST /cuotas/<id>/pagar
Parámetros: id de la cuota en URL
Retorna: Redirect a /prestamos/<id>
Efecto: Marca cuota como PAGADA
         Registra fecha de pago
         Si todas pagadas, marca préstamo como CANCELADO
```

#### 5. API JSON (para cálculos frontend)

```
POST /api/calcular-cuota
Content-Type: application/json

Request:
{
  "monto": 100000,
  "tasa_interes": 15.5,
  "cantidad_cuotas": 24
}

Response:
{
  "cuota": 4415.07
}

Uso: Usado en JavaScript para mostrar cuota en tiempo real
```

#### 6. Reportes

```
GET /reportes
Retorna: Página con reporte de préstamos
Datos: Lista completa de préstamos con estado

GET /consultas
Retorna: Página de consultas avanzadas
Parámetros: 
  ?cliente_id=1 (opcional)
  ?estado=ACTIVO (opcional)
Ejemplo: /consultas?cliente_id=1&estado=ACTIVO
```

### Formato de responses

**Éxito (HTML):**
```
HTTP 200 OK
Content-Type: text/html
Body: Página HTML con datos
```

**Éxito (JSON):**
```
HTTP 200 OK
Content-Type: application/json
Body: {"cuota": 4415.07}
```

**Error 404:**
```
HTTP 404 Not Found
Body: Página "no encontrada"
```

**Error 500:**
```
HTTP 500 Internal Server Error
Body: Página "Error del servidor"
```

**Redirect (después POST):**
```
HTTP 302 Found
Location: /clientes
```

---

## Base de Datos

### Esquema de tablas

#### Tabla `clientes`

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

CREATE INDEX idx_clientes_documento ON clientes(documento);
CREATE INDEX idx_clientes_nombre ON clientes(nombre);
```

**Campos:**
- `id`: Identificador único (autoincrementado)
- `nombre`: Nombre del cliente (requerido, max 100 chars)
- `apellido`: Apellido (requerido)
- `documento`: Cédula/RUC (único, max 20 chars)
- `telefono`: Número de teléfono (opcional)
- `correo`: Email (opcional)
- `direccion`: Domicilio (opcional)
- `fecha_registro`: Fecha de registro automática

#### Tabla `prestamos`

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

CREATE INDEX idx_prestamos_cliente ON prestamos(cliente_id);
CREATE INDEX idx_prestamos_estado ON prestamos(estado);
CREATE INDEX idx_prestamos_fecha ON prestamos(fecha_desembolso);
```

**Campos:**
- `id`: Identificador único
- `cliente_id`: Referencia al cliente (FK)
- `monto`: Capital prestado (12 dígitos, 2 decimales)
- `tasa_interes`: Tasa anual %
- `cantidad_cuotas`: Número de meses
- `fecha_desembolso`: Fecha de desembolso
- `estado`: ACTIVO o CANCELADO
- `fecha_creacion`: Timestamp automático
- `cuota_mensual`: Cuota calculada
- `interes_total`: Total de intereses
- `monto_total`: Capital + intereses

#### Tabla `cuotas`

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

CREATE INDEX idx_cuotas_prestamo ON cuotas(prestamo_id);
CREATE INDEX idx_cuotas_estado ON cuotas(estado);
CREATE INDEX idx_cuotas_fecha_vencimiento ON cuotas(fecha_vencimiento);
```

**Campos:**
- `numero_cuota`: 1, 2, 3... hasta n
- `fecha_vencimiento`: Cuándo vence la cuota
- `capital`: Porción de capital en esta cuota
- `interes`: Interés generado en esta cuota
- `monto_cuota`: Total a pagar (capital + interés)
- `saldo_restante`: Capital pendiente después de pagar
- `estado`: PENDIENTE o PAGADO
- `fecha_pago`: Cuándo se pagó (NULL si PENDIENTE)

#### Tabla `pagos`

```sql
CREATE TABLE pagos (
  id SERIAL PRIMARY KEY,
  cuota_id INTEGER NOT NULL REFERENCES cuotas(id) ON DELETE CASCADE,
  fecha_pago TIMESTAMP DEFAULT now(),
  monto_pagado NUMERIC(15, 2) NOT NULL,
  observacion VARCHAR(200)
);

CREATE INDEX idx_pagos_cuota ON pagos(cuota_id);
CREATE INDEX idx_pagos_fecha ON pagos(fecha_pago);
```

**Campos:**
- `monto_pagado`: Cantidad pagada
- `observacion`: Notas (cheque número, referencia, etc.)
- `fecha_pago`: Timestamp del pago

### Relaciones

```
Clientes (1) ─── (N) Préstamos
  ↓ id           ↓ cliente_id

Préstamos (1) ─── (N) Cuotas
  ↓ id            ↓ prestamo_id

Cuotas (1) ─── (N) Pagos
  ↓ id      ↓ cuota_id
```

### Backups y mantenimiento

**Backup de base de datos:**
```bash
# Completo
pg_dump -U prestamo_user -h localhost sistema_prestamo > backup.sql

# Solo datos
pg_dump -U prestamo_user --data-only -h localhost sistema_prestamo > data_backup.sql

# Programado diario
crontab -e
# 0 2 * * * pg_dump -U prestamo_user sistema_prestamo > /backups/sistema_$(date +\%Y\%m\%d).sql
```

**Restaurar base de datos:**
```bash
psql -U prestamo_user -h localhost sistema_prestamo < backup.sql
```

---

## Guía de Administración

### Primeros pasos

1. **Crear usuario administrador** (Falta implementar)
2. **Registrar primeros clientes**
3. **Crear préstamos de prueba**
4. **Verificar cálculos**

### Monitoreo

**Ver estado de la aplicación:**
```bash
# Ver logs
tail -f app.log

# Ver conexiones PostgreSQL
psql -c "SELECT * FROM pg_stat_activity;" sistema_prestamo

# Ver tamaño de BD
psql -c "SELECT pg_size_pretty(pg_database_size('sistema_prestamo'));"
```

### Mantenimiento

**Limpiar logs:**
```bash
rm app.log
```

**Vacío de base de datos** (eliminar todo):
```bash
python reset_db.py
```

**Verificar integridad:**
```bash
# Chequear que saldos finales = 0
psql -c "SELECT prestamo_id, COUNT(*) FROM cuotas GROUP BY prestamo_id HAVING COUNT(*) > 60;"
```

---

## Mejoras Futuras

### Fase 2 (Próximas 6 meses)

- ✅ Autenticación de usuarios (login/logout)
- ✅ Rol de administrador vs usuario
- ✅ Contraseñas hasheadas (bcrypt)
- ✅ Validación de entrada robusta (WTForms)
- ✅ Tests unitarios con pytest
- ✅ Documentación Swagger para API
- ✅ Paginación en listados
- ✅ Exportación a PDF de cronogramas
- ✅ Notificaciones por email de cuotas próximas

### Fase 3 (6-12 meses)

- 🔄 Integración con pasarelas de pago (PayPal, Stripe, Moneyweb)
- 🔄 Dashboard avanzado con Grafana
- 🔄 Alertas automáticas de mora
- 🔄 Cálculo de comisiones y seguros
- 🔄 Módulo de refinanciación
- 🔄 Soporte multi-moneda
- 🔄 Integración con entidades regulatorias (SIB)
- 🔄 App móvil (React Native)

### Fase 4 (12+ meses)

- 🚀 Machine Learning para scoring de crédito
- 🚀 Análisis predictivo de mora
- 🚀 Blockchain para auditoría inmutable
- 🚀 API pública para terceros
- 🚀 Marketplace de productos financieros

---

## Problemas conocidos y limitaciones

### Limitaciones actuales

1. **Sin autenticación** - Cualquiera accede a cualquier datos
2. **Sin audit trail** - No se registra quién hizo qué cambios
3. **Moneda fija** - Solo guaraní, no soporta múltiples divisas
4. **Sin intereses compuestos** - Solo sistema francés
5. **Sin cuotas variables** - Todas las cuotas son iguales
6. **Edición de préstamos elimina cuotas** - Pierde historial

### Bugs conocidos

- Redondeo de cuotas puede variar en 1-2 centavos en última cuota (se ajusta automáticamente)
- Sin validación de fechas futuras en formularios

### Performance

- Sin problemas hasta 100,000 registros
- Recomendado agregar caché para dashboard si > 1,000,000 registros
- Agregar índices adicionales si % queries aumenta

---

## Soporte y contacto

- **Email**: soporte@sistemaprestamos.com
- **Issues**: GitHub Issues
- **Documentación**: Ver ANALISIS_PROFESIONAL.md
- **Guía de desarrollo**: Ver CONTRIBUTING.md (no incluida)

---

## Licencia

Este proyecto está bajo licencia MIT. Puedes usarlo, modificarlo y distribuirlo libremente.

```
MIT License

Copyright (c) 2026 Sistema de Gestión de Préstamos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## Versión del proyecto

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0.0 | 22/06/2026 | Versión inicial - Funcionalidad completa |
| 0.9.0 | 17/06/2026 | Beta testing |
| 0.1.0 | 01/06/2026 | Prototipo inicial |

---

## Roadmap visual

```
2026 Jun  Aug     Oct     Dec
 |    |     |       |      |
 ├─ v1.0 ────────────────────  Autenticación
 │    ├─ Tests
 │    ├─ Validación robusta
 │    └─ Swagger API
 │
 └─ v2.0                      Integraciones
      ├─ PayPal/Stripe
      ├─ Gráficos avanzados
      ├─ Alertas de mora
      └─ PDF exports

2027 ───────────────────────────
      ├─ v3.0: ML + Scoring
      └─ v4.0: App móvil
```

---

**Última actualización:** 22 de junio de 2026

*Documento generado como parte de auditoría académica profesional del proyecto.*

