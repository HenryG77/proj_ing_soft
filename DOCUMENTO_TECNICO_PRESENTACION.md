# Documento técnico de presentación
# Sistema de Gestión de Préstamos con Flask, SQLAlchemy y templates

## Índice

1. Introducción del proyecto
2. Capítulo 1 – ORM (Object Relational Mapping)
3. Capítulo 2 – Arquitectura MVC
4. Capítulo 3 – Instalación del proyecto
5. Capítulo 4 – Sistema de créditos
6. Capítulo 5 – Sistema Francés de Amortización
7. Capítulo 6 – Cálculo de la cuota mensual
8. Capítulo 7 – Redondeo de las cuotas
9. Capítulo 8 – Cálculo de fechas
10. Capítulo 9 – Explicación del código del proyecto
11. Capítulo 10 – Preparación para la exposición
12. Conclusiones
13. Recomendaciones

---

## 1. Introducción del proyecto

El sistema objeto de estudio es una aplicación web orientada a la gestión integral de préstamos, desarrollada con Flask como framework de backend, SQLAlchemy como ORM y plantillas HTML para la capa de presentación. Su propósito principal es automatizar el proceso completo de administración de créditos, desde la captura de clientes hasta la generación automática de cuotas y cronogramas de pago.

### 1.1 Objetivo del sistema

El objetivo general del sistema es proporcionar una herramienta que permita registrar clientes, crear préstamos, calcular cuotas de manera automática, generar cronogramas de pago, registrar pagos y visualizar reportes o estados operativos. En términos más amplios, el sistema busca reducir la intervención manual en procesos financieros, minimizar errores de cálculo y mejorar la trazabilidad de las operaciones.

### 1.2 Problema que resuelve

En entornos reales de microfinanzas, cooperativas, fondos de empleados o instituciones crediticias, el manejo manual de préstamos suele presentar problemas como:

- errores en los cálculos de intereses y cuotas;
- pérdida de control sobre el saldo pendiente;
- dificultades para generar cronogramas de pago;
- falta de trazabilidad de pagos realizados;
- procesos lentos y dependientes de hojas de cálculo o registros aislados.

El sistema resuelve estos problemas al centralizar la información y automatizar el cálculo financiero.

### 1.3 Arquitectura general

El sistema sigue una arquitectura sencilla pero sólida basada en capas:

- Capa de presentación: templates HTML y Bootstrap.
- Capa de aplicación: Flask con rutas y controladores.
- Capa de negocio: reglas para creación de préstamos, cálculo de cuotas y generación de cronogramas.
- Capa de persistencia: SQLAlchemy y una base de datos relacional.

La organización básica es la siguiente:

```text
Usuario
  ↓
Navegador
  ↓
Flask (app.py)
  ↓
Rutas / Controladores
  ↓
Modelos ORM (models.py)
  ↓
Base de datos relacional
  ↓
Vistas / Templates
  ↓
Respuesta HTML al navegador
```

### 1.4 Tecnologías utilizadas

El proyecto utiliza las siguientes tecnologías:

- Python como lenguaje principal.
- Flask como framework web ligero.
- Flask-SQLAlchemy como ORM.
- PostgreSQL como motor de base de datos relacional.
- Jinja2 como motor de plantillas.
- Bootstrap para el diseño de la interfaz.
- python-dotenv para la gestión de variables de entorno.

### 1.5 Flujo completo del sistema

El flujo general es el siguiente:

1. El usuario accede a una ruta del sistema, por ejemplo /prestamos o /clientes.
2. Flask recibe la solicitud.
3. La ruta ejecuta la lógica correspondiente.
4. El controlador consulta o modifica datos a través del ORM.
5. El ORM convierte las operaciones en consultas SQL hacia la base de datos.
6. La respuesta se prepara y se entrega a una plantilla.
7. La plantilla renderiza el resultado en HTML.
8. El navegador muestra la información al usuario.

En el caso específico del registro de un préstamo, el flujo es más detallado:

```text
Usuario completa formulario
  ↓
Ruta /prestamos/nuevo
  ↓
Controlador crea objeto Prestamo
  ↓
ORM persiste el préstamo
  ↓
Se invoca la generación del cronograma
  ↓
Se calculan cuotas, intereses y saldos
  ↓
Se almacenan las cuotas en la base de datos
  ↓
Se redirige a la vista de préstamos
```

---

# CAPÍTULO 1 – ORM (Object Relational Mapping)

## 1.1 Qué es un ORM

Un ORM es una capa de abstracción que permite interactuar con una base de datos relacional utilizando objetos y clases del lenguaje de programación, en lugar de escribir manualmente sentencias SQL. En lugar de pensar en tablas, filas y columnas, el desarrollador trabaja con entidades como Cliente, Prestamo, Cuota y Pago.

El ORM se encarga de traducir operaciones como crear, leer, actualizar o eliminar objetos a instrucciones SQL comprensibles para el motor de base de datos.

### Idea central

El objetivo del ORM es reducir la brecha entre el paradigma orientado a objetos y el paradigma relacional.

```text
Programación orientada a objetos
  ↓
Objetos y clases
  ↓
ORM
  ↓
Relaciones y tablas en la base de datos
```

## 1.2 Problemas que resuelve un ORM

Un ORM resuelve varias problemáticas típicas:

- Evita escribir SQL repetitivo y propenso a errores.
- Hace más legible el código.
- Reduce el acoplamiento con un motor de base de datos concreto.
- Permite cambiar de motor con menos impacto si la abstracción se usa correctamente.
- Facilita la implementación de relaciones entre entidades.
- Mejora la seguridad al evitar SQL manual y concatenaciones inseguras.

## 1.3 Cómo evita escribir SQL manual

Sin ORM, una operación simple como registrar un cliente podría implicar algo como:

```sql
INSERT INTO clientes (nombre, apellido, documento, telefono)
VALUES ('Juan', 'Pérez', '1234567', '0981-111111');
```

Con ORM, el código se expresa de forma más natural en Python:

```python
cliente = Cliente(nombre='Juan', apellido='Pérez', documento='1234567')
db.session.add(cliente)
db.session.commit()
```

El ORM traduce esa instrucción en la consulta apropiada según el motor de base de datos configurado.

## 1.4 Cómo transforma objetos en registros

El ORM trabaja con dos niveles de representación:

1. Representación en memoria: objetos Python.
2. Representación persistida: tablas y filas en la base de datos.

Cuando se crea un objeto de tipo Cliente, el ORM lo convierte en una fila de la tabla clientes. Cuando se modifica un atributo de ese objeto, el ORM detecta el cambio y lo refleja en la operación de actualización.

### Ejemplo conceptual

```python
cliente = Cliente(nombre='Ana', apellido='Gómez', documento='7654321')
```

Esto no es solo un objeto en memoria; el ORM puede interpretarlo como una entidad del modelo de datos que será persistida en la tabla correspondiente.

## 1.5 Mapeo entre clases y tablas

En este proyecto, las clases del archivo [models.py](models.py) representan tablas de la base de datos.

Por ejemplo:

- Cliente → tabla clientes
- Prestamo → tabla prestamos
- Cuota → tabla cuotas
- Pago → tabla pagos

Este patrón se conoce como mapeo de clases a tablas.

### Ejemplo de mapeo

```python
class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
```

Aquí se observa que:

- la clase Cliente representa la entidad Cliente;
- la tabla se declara con __tablename__;
- cada atributo de la clase corresponde a una columna de la tabla.

## 1.6 Tipos de relaciones

### 1.6.1 One to One

Una entidad A se relaciona con una única entidad B, y viceversa.

Ejemplo conceptual:

- una persona tiene un perfil único;
- un perfil pertenece a una sola persona.

En el proyecto no se usa explícitamente este tipo de relación, pero es relevante para comprender el modelo conceptual.

### 1.6.2 One to Many

Una entidad A puede tener muchas entidades B, pero cada B pertenece a un solo A.

Ejemplo clásico:

- un cliente puede tener muchos préstamos;
- cada préstamo pertenece a un cliente.

En este proyecto se representa con:

```python
class Cliente(db.Model):
    prestamos = db.relationship('Prestamo', backref='cliente', lazy=True)
```

y en Prestamo:

```python
cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
```

### 1.6.3 Many to One

Es la misma idea vista desde el lado opuesto. Muchas entidades B pertenecen a una entidad A.

En este sistema, muchas cuotas pertenecen a un mismo préstamo; muchas pagos pertenecen a una misma cuota. Es un patrón muy común en bases de datos transaccionales.

### 1.6.4 Many to Many

Muchas entidades A pueden estar relacionadas con muchas entidades B.

Ejemplo típico:

- estudiantes y cursos;
- usuarios y roles.

No es el caso del proyecto actual, pero es importante entender el concepto porque aparece frecuentemente en sistemas empresariales.

## 1.7 Ventajas del ORM

- Menos SQL manual.
- Código más limpio y mantenible.
- Menor riesgo de errores de sintaxis.
- Mayor productividad.
- Mejor integración con el lenguaje de programación.

## 1.8 Desventajas del ORM

- Puede generar consultas menos óptimas en algunos casos.
- El desarrollador debe entender cómo funciona para no caer en consultas innecesarias.
- Algunas operaciones complejas pueden requerir SQL puro.
- El aprendizaje inicial puede ser más abstracto que escribir SQL directamente.

## 1.9 Rendimiento y seguridad

### Rendimiento

El ORM puede ser muy eficiente cuando se usa correctamente. Sin embargo, si se hacen consultas innecesarias o se cargan relaciones de forma agresiva, el rendimiento puede degradarse. Por ello se recomienda usar lazy loading con criterio y evitar N+1 queries.

### Seguridad

Un ORM reduce sustancialmente el riesgo de inyección SQL porque evita la concatenación directa de texto. Aun así, se deben aplicar buenas prácticas como:

- validar entradas del usuario;
- no confiar en datos provenientes del navegador;
- usar parámetros y filtros seguros.

## 1.10 Buenas prácticas con ORM

- Mantener el modelo limpio y expresivo.
- Usar nombres claros para entidades y columnas.
- Evitar lógica de negocio dentro de los modelos cuando no corresponde.
- Cuidar la carga de relaciones.
- Usar migraciones cuando el esquema evoluciona.
- Documentar las reglas de negocio.

## 1.11 Ejemplo antes y después del ORM

### Antes: SQL manual

```sql
SELECT * FROM prestamos WHERE estado = 'ACTIVO';
```

### Después: ORM

```python
prestamos = Prestamo.query.filter_by(estado='ACTIVO').all()
```

Esta diferencia es muy importante porque el código Python es más expresivo y más fácil de mantener.

## 1.12 Uso del ORM en este proyecto

El archivo [models.py](models.py) define las entidades del sistema y sus relaciones. La aplicación en [app.py](app.py) usa esas entidades para crear, consultar y modificar datos sin escribir SQL manual en la mayor parte del flujo. El archivo [database.py](database.py) centraliza la inicialización de SQLAlchemy y la conexión a la base de datos.

---

# CAPÍTULO 2 – Arquitectura MVC

## 2.1 Qué es MVC

MVC es un patrón de arquitectura de software que separa la aplicación en tres componentes principales:

- Modelo: representa la información y la lógica de negocio.
- Vista: se encarga de mostrar información al usuario.
- Controlador: recibe las entradas y coordina el flujo entre modelo y vista.

## 2.2 Router

El router es la parte encargada de recibir las peticiones del usuario y determinar qué controlador debe ejecutar.

En Flask, las rutas se registran con decoradores, por ejemplo:

```python
@app.route('/prestamos')
def prestamos():
    ...
```

### Función del router

- recibe la URL solicitada;
- identifica el endpoint correspondiente;
- extrae parámetros si existen;
- invoca la función o controlador asociado.

### Flujo del router

```text
Usuario
  ↓
Solicitud HTTP
  ↓
Flask Router
  ↓
Función asociada a la ruta
  ↓
Controlador
```

## 2.3 Controlador

En este proyecto, el controlador está implementado en [app.py](app.py). Allí se encuentra gran parte de la lógica de negocio, incluida la creación de clientes, préstamos, cálculo de cuotas y generación de cronogramas.

### Responsabilidades del controlador

- recibir datos del formulario;
- validar entradas;
- consultar o persistir datos con el ORM;
- preparar variables para la vista;
- renderizar una plantilla o redirigir a otra ruta.

### Importancia de la separación

La lógica de negocio no debe ir en la vista porque la vista tiene como responsabilidad mostrar información, no decidir cómo debe comportarse el sistema.

## 2.4 Template / View

Las vistas están en la carpeta [templates](templates). Son archivos HTML que contienen estructura y, en algunos casos, lógica de renderizado con Jinja2.

### Qué es una plantilla

Una plantilla es un archivo que describe cómo se mostrará la interfaz. Puede recibir variables desde el controlador y representarlas en pantalla.

### Ejemplo simple

```html
<h1>Bienvenido, {{ nombre }}</h1>
```

Aquí el símbolo {{ }} se usa para imprimir una variable.

### Sintaxis de Jinja2

- {{ variable }}: imprime una variable.
- {% if condicion %}...{% endif %}: estructura de control.
- {% for elemento in lista %}...{% endfor %}: recorrido de listas.
- {% extends "base.html" %}: herencia de layout.
- {% block content %}...{% endblock %}: bloques reutilizables.

### Diferencia entre imprimir y controlar

- Imprimir variables: se usa con {{ }}.
- Ejecutar lógica: se usa con {% %}.

Esto es fundamental para mantener la vista limpia y legible.

### Layout y herencia

El proyecto usa [templates/base.html](templates/base.html) como plantilla base. Otras vistas, como [templates/dashboard.html](templates/dashboard.html), heredan de esa estructura. Esto permite reutilizar cabeceras, barras laterales y estilos comunes.

### Flujo Controller → View

```text
Controlador prepara datos
  ↓
render_template('clientes.html', clientes=clientes)
  ↓
Vista recibe variables
  ↓
HTML generado con Jinja2
```

### Por qué no hacer cálculos en la vista

Porque la vista debe ser un componente de presentación poco complejo. Si en la vista se calculan intereses, se modifican saldos o se interpretan reglas de negocio, se rompe la separación de responsabilidades y el código se vuelve difícil de mantener.

---

# CAPÍTULO 3 – Instalación del proyecto

## 3.1 Requisitos previos

Antes de instalar el proyecto, se recomienda contar con:

- Python 3.10 o superior.
- pip actualizado.
- acceso a una terminal.
- una base de datos PostgreSQL disponible.
- permisos para crear bases de datos y usuarios.

## 3.2 Instalación del lenguaje

En Windows, se recomienda descargar Python desde el sitio oficial y marcar la opción de agregar Python al PATH durante la instalación.

Verificación:

```powershell
python --version
```

## 3.3 Instalación del gestor de paquetes

pip suele venir incluido con Python. Para verificar:

```powershell
pip --version
```

## 3.4 Creación del entorno virtual

Es buena práctica trabajar con un entorno virtual para aislar dependencias del proyecto.

```powershell
python -m venv venv
```

Activación en Windows PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

## 3.5 Instalación de dependencias

El archivo [requirements.txt](requirements.txt) contiene las dependencias del proyecto. Para instalarlas:

```powershell
pip install -r requirements.txt
```

### Dependencias clave

- Flask
- Flask-SQLAlchemy
- psycopg2-binary
- python-dotenv

## 3.6 Configuración del archivo de entorno

El proyecto usa variables de entorno para la conexión a la base de datos. En general se requiere un archivo .env con una variable DATABASE_URL.

Ejemplo:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sistema_prestamo
```

## 3.7 Configuración de la base de datos

Debe existir una base de datos PostgreSQL llamada sistema_prestamo o el nombre indicado en la variable de entorno.

Verificación simple:

```sql
CREATE DATABASE sistema_prestamo;
```

## 3.8 Generación del esquema

Al iniciar la aplicación, el sistema crea las tablas automáticamente mediante SQLAlchemy.

En [database.py](database.py) se define la inicialización de la base de datos y la creación del esquema.

## 3.9 Ejecución del proyecto

Una vez instaladas las dependencias, se puede ejecutar:

```powershell
python app.py
```

Si todo está bien, Flask mostrará la dirección local donde la aplicación está siendo servida, normalmente:

```text
http://127.0.0.1:5000
```

## 3.10 Verificación del funcionamiento

Se pueden probar rutas como:

- /
- /clientes
- /prestamos
- /reportes
- /consultas

## 3.11 Buenas prácticas durante la instalación

- No usar el sistema Python global si se puede evitar.
- Mantener las dependencias en un archivo reproducible.
- Documentar los valores del archivo .env.
- Comprobar que la base de datos está accesible antes de arrancar la app.

---

# CAPÍTULO 4 – Sistema de Créditos

## 4.1 Qué es un crédito

Un crédito es un contrato financiero mediante el cual una entidad otorga un monto de dinero a un cliente, quien se compromete a devolverlo en un plazo determinado, generalmente con un costo financiero asociado: el interés.

## 4.2 Componentes del crédito

### Capital

Es el monto inicial prestado. En este proyecto se almacena como monto del préstamo.

### Interés

Es el costo del dinero prestado. Se expresa normalmente como porcentaje anual.

### Plazo

Es el tiempo de devolución del préstamo, medido en cuotas.

### Tasa anual

Es la tasa aplicada sobre el capital durante un año. En el sistema se registra como tasa_interes.

### Tasa mensual

Para calcular cuotas periódicas, la tasa anual debe convertirse a tasa mensual.

La relación es:

$$
 i_m = \frac{i_a}{12} 
$$

donde:

- $i_m$ es la tasa mensual;
- $i_a$ es la tasa anual.

### Saldo

Es el monto que aún falta por pagar después de aplicar cada cuota.

### Amortización

Es la parte del pago que reduce el capital original del préstamo.

### Interés generado

Es la parte del pago que corresponde al costo financiero por el uso del dinero.

### Pago

Es la cantidad total que debe cancelarse en cada periodo.

### Saldo pendiente

Es el capital que todavía no ha sido amortizado.

## 4.3 Relación entre los conceptos

En cada periodo:

$$
\text{Cuota} = \text{Interés} + \text{Amortización}
$$

Y además:

$$
\text{Saldo nuevo} = \text{Saldo anterior} - \text{Amortización}
$$

Este vínculo es esencial para entender cómo funciona un sistema de amortización.

---

# CAPÍTULO 5 – Sistema Francés de Amortización

## 5.1 Historia y fundamento

El sistema francés de amortización es uno de los métodos más utilizados en financiamiento, especialmente en créditos hipotecarios, personales y empresariales. Su característica principal es que las cuotas son constantes en valor, aunque la proporción entre interés y capital cambia en cada periodo.

## 5.2 Por qué las cuotas son constantes

La cuota permanece igual para todos los periodos porque el préstamo se devuelve en pagos periódicos equivalentes. Al inicio, la mayor parte de la cuota corresponde a interés; al final, la mayor parte corresponde a capital.

## 5.3 Qué sucede en cada cuota

En cada periodo:

1. Se calcula el interés sobre el saldo pendiente.
2. Se determina la amortización como la diferencia entre la cuota y el interés.
3. Se reduce el saldo pendiente.
4. Se repite el proceso hasta terminar el préstamo.

## 5.4 Fórmula matemática

La fórmula del sistema francés es:

$$
C = P \cdot \frac{i(1+i)^n}{(1+i)^n - 1}
$$

Donde:

- $C$ = cuota periódica constante;
- $P$ = monto del préstamo o capital inicial;
- $i$ = tasa de interés periódica;
- $n$ = número de cuotas.

## 5.5 Significado de cada variable

- $P$: valor inicial del crédito.
- $i$: tasa mensual, expresada en forma decimal.
- $n$: cantidad de periodos.
- $C$: pago fijo que debe realizarse cada periodo.

## 5.6 Desarrollo paso a paso

La fórmula se puede explicar de la siguiente manera:

1. Se calcula el factor de acumulación $(1+i)^n$.
2. Se multiplica por la tasa $i$.
3. Se divide por $(1+i)^n - 1$.
4. El resultado se multiplica por el capital $P$.

Este proceso genera una cuota fija que, aplicada repetidamente, amortiza el crédito completamente.

## 5.7 Ejemplo completo

Supongamos:

- Capital $P = 1000$
- Tasa anual = 12%
- Tasa mensual $i = 0.01$
- Número de cuotas $n = 3$

Aplicando la fórmula:

$$
C = 1000 \cdot \frac{0.01(1.01)^3}{(1.01)^3 - 1}
$$

Resolviendo:

$$
(1.01)^3 = 1.030301
$$

$$
C = 1000 \cdot \frac{0.01 \cdot 1.030301}{1.030301 - 1}
$$

$$
C = 1000 \cdot \frac{0.01030301}{0.030301}
$$

$$
C \approx 339.99
$$

En la práctica, con redondeos y ajustes, el valor puede variar ligeramente, pero la idea es la misma.

## 5.8 Tabla de amortización

Una tabla de amortización contiene las siguientes columnas:

| Columna | Significado |
|---|---|
| Número de cuota | Identificador del periodo |
| Fecha de vencimiento | Fecha en que debe pagarse |
| Interés | Costo financiero del periodo |
| Amortización | Parte que reduce el capital |
| Cuota | Pago total del periodo |
| Saldo | Capital pendiente |

## 5.9 Relación con el proyecto

El método se implementa en [models.py](models.py) a través del método que genera el cronograma. Allí se calcula la cuota, se determinan los intereses, se actualiza el saldo y se construye la tabla de cuotas.

---

# CAPÍTULO 6 – Cálculo de la cuota mensual

## 6.1 Paso 1: conversión de tasa anual a mensual

La tasa anual debe convertirse a una tasa periódica equivalente para cada cuota.

$$
 i_m = \frac{tasa\_anual}{100 \cdot 12}
$$

## 6.2 Paso 2: aplicación de la fórmula francesa

Se sustituye la tasa mensual en la fórmula:

$$
C = P \cdot \frac{i_m(1+i_m)^n}{(1+i_m)^n - 1}
$$

## 6.3 Paso 3: obtención de la cuota

El resultado de esa fórmula es la cuota mensual teórica. En el sistema, este valor se redondea o se ajusta para evitar diferencias de centavos.

## 6.4 Paso 4: cálculo del interés

Para cada cuota:

$$
\text{Interés} = \text{Saldo anterior} \times i_m
$$

## 6.5 Paso 5: cálculo de amortización

$$
\text{Amortización} = \text{Cuota} - \text{Interés}
$$

## 6.6 Paso 6: actualización del saldo

$$
\text{Saldo nuevo} = \text{Saldo anterior} - \text{Amortización}
$$

## 6.7 Paso 7: repetición del proceso

Este ciclo se repite para cada una de las cuotas del crédito hasta que el saldo llegue a cero.

## 6.8 Importancia de este proceso

El cálculo correcto de la cuota no solo afecta la transparencia del crédito, sino también la integridad del sistema financiero. Un error en este proceso puede generar diferencias de saldo, sobrepagos o subpagos.

---

# CAPÍTULO 7 – Redondeo de las cuotas

## 7.1 Problemas de precisión decimal

En los sistemas financieros, los valores monetarios deben manejarse con precisión. Si se usan tipos flotantes, pueden aparecer errores como:

```text
1000.10 + 0.20 = 1000.3000000004
```

Por esa razón, es preferible trabajar con decimales exactos.

## 7.2 Error por redondeo sucesivo

Si en cada cuota se redondea directamente al centavo, la suma de ellas puede no coincidir con el monto real del préstamo. Este problema es muy común en sistemas de amortización.

## 7.3 Diferencia entre truncar y redondear

- Redondear: ajusta al valor más cercano.
- Truncar: elimina los decimales adicionales sin aproximar.

En este proyecto se adoptó una estrategia de control del residuo para que el saldo final cierre correctamente.

## 7.4 Por qué las cuotas deben ser exactas

Una cuota debe reflejar de forma confiable el valor de la operación financiera. Si cada cuota pierde centavos, al final se acumula un error que puede afectar el saldo y la última cuota.

## 7.5 Ajuste de la última cuota

Una metodología frecuente consiste en:

1. calcular la cuota con precisión total;
2. redondear solo para efectos de presentación o registro;
3. acumular el residuo;
4. ajustar la última cuota para que el saldo final sea cero.

## 7.6 Ejemplo práctico

Supongamos que la cuota teórica es 150000.56 y la siguiente es 150000.56. Si se redondea cada una a 150000.00, se pierde 0.56 en cada periodo. Esa diferencia puede acumularse y afectar al final del crédito.

Por eso la lógica correcta es preservar el residuo y usarlo para el ajuste final.

## 7.7 Aplicación en este proyecto

La mejora implementada en [models.py](models.py) busca conservar el ajuste de centavos y evitar que el saldo quede desfasado. La lógica asegura que la suma de las cuotas y el saldo pendiente cierren correctamente.

---

# CAPÍTULO 8 – Cálculo de fechas

## 8.1 Importancia de las fechas de vencimiento

Las fechas de vencimiento son fundamentales para la operación del sistema. Determinan cuándo debe pagarse cada cuota y permiten organizar la cobranza.

## 8.2 Cómo se generan las fechas

El sistema toma la fecha de desembolso del préstamo y calcula la fecha siguiente para cada periodo. En el caso mensual, se suma un mes a la fecha anterior.

## 8.3 Qué ocurre si el día es domingo

Si la fecha calculada cae en domingo, se recomienda moverla al lunes siguiente para que sea un día hábil. Esta regla es útil en sistemas bancarios y financieros, donde los vencimientos suelen evitarse en fines de semana.

## 8.4 Algoritmo paso a paso

1. Se toma la fecha base del préstamo.
2. Se suma un mes.
3. Se verifica si la fecha resultante corresponde a domingo.
4. Si es domingo, se suma un día.
5. Se guarda la fecha de vencimiento.

## 8.5 Ejemplo práctico

Si el primer vencimiento cae en domingo, se ajusta al lunes siguiente.

Ejemplo:

```text
Fecha base: 2026-01-04
Día: domingo
Vencimiento ajustado: 2026-01-05
```

## 8.6 Aplicación en este proyecto

En [models.py](models.py) se implementa una lógica que calcula la siguiente fecha de pago y, si esta corresponde a domingo, la corrige para que sea hábil.

---

# CAPÍTULO 9 – Explicación del código del proyecto

## 9.1 Estructura general

El proyecto está organizado de manera sencilla:

```text
proj_ing_soft/
├── app.py
├── database.py
├── models.py
├── requirements.txt
├── reset_db.py
├── templates/
│   ├── base.html
│   ├── clientes.html
│   ├── consultas.html
│   ├── cronograma.html
│   ├── dashboard.html
│   ├── prestamos.html
│   └── reportes.html
└── README.md
```

## 9.2 Archivo app.py

Este archivo es el punto de entrada de la aplicación Flask. Aquí se define la instancia de la aplicación, se inicializa la base de datos y se registran las rutas.

### Responsabilidades principales

- crear la app Flask;
- cargar la configuración;
- inicializar SQLAlchemy;
- definir rutas para clientes, préstamos, reportes y consultas;
- renderizar templates con los datos obtenidos.

## 9.3 Archivo database.py

Este archivo centraliza la configuración de la base de datos. Se encarga de:

- cargar variables de entorno;
- construir la URL de conexión;
- inicializar SQLAlchemy;
- crear las tablas al arrancar la app.

## 9.4 Archivo models.py

Es el corazón del modelo de datos. Aquí se definen las clases que representan las entidades del negocio.

### Clases principales

- Cliente: representa a un cliente.
- Prestamo: representa un préstamo.
- Cuota: representa cada cuota del cronograma.
- Pago: representa un pago realizado sobre una cuota.

Además, aquí se implementa la lógica para generar el cronograma y los cálculos financieros.

## 9.5 Carpeta templates

Contiene las vistas HTML. La plantilla base [templates/base.html](templates/base.html) define la estructura general de navegación y estilos. Las demás vistas complementan el contenido específico de cada sección.

## 9.6 Flujo completo de una operación real

### Ejemplo: crear un préstamo

1. El usuario accede a la ruta /prestamos/nuevo.
2. El controlador prepara la lista de clientes.
3. Se muestra el formulario con los datos requeridos.
4. El usuario envía la información.
5. El controlador recibe el formulario.
6. Se construye un objeto Prestamo.
7. El ORM lo persiste en la base de datos.
8. Se genera el cronograma de cuotas.
9. Se redirige a la lista de préstamos.

## 9.7 Relación entre archivos

```text
app.py
  └── usa modelos de models.py
  └── renderiza templates
models.py
  └── define entidades y lógica financiera
database.py
  └── configura conexión y creación de tablas
templates/
  └── muestran el resultado al usuario
```

---

# CAPÍTULO 10 – Preparación para la exposición

## 10.1 Qué decir en la introducción

La introducción debe responder a tres preguntas básicas:

1. ¿Qué problema resuelve el sistema?
2. ¿Por qué es útil?
3. ¿Cómo está organizado internamente?

Una buena introducción podría ser:

> El sistema que presentamos modela el proceso de gestión de créditos desde la captura del cliente hasta la generación de cuotas y pagos, utilizando una arquitectura web simple y un modelo de datos relacional que permite automatizar cálculos y mantener la información organizada.

## 10.2 Cómo explicar el ORM

Se recomienda explicar que el ORM permite trabajar con objetos en lugar de consultas manuales. Puede decirse:

> El ORM actúa como un traductor entre el mundo orientado a objetos y el mundo relacional. En lugar de escribir manualmente SQL, trabajamos con clases y objetos que el sistema convierte en tablas y registros.

## 10.3 Cómo explicar las rutas

Se debe destacar que las rutas son el punto de entrada de la aplicación y que cada una representa una funcionalidad concreta.

## 10.4 Cómo explicar el controlador

El controlador debe presentarse como el componente que recibe la solicitud, consulta datos, ejecuta reglas y prepara la respuesta.

## 10.5 Cómo explicar las vistas

Las vistas deben explicarse como la capa de presentación. Su labor es mostrar información, no tomar decisiones complejas sobre la lógica del negocio.

## 10.6 Cómo explicar la instalación

La instalación debe presentarse como un proceso paso a paso. Es conveniente mostrar:

- creación del entorno virtual;
- instalación de dependencias;
- configuración del archivo .env;
- ejecución de la aplicación.

## 10.7 Cómo explicar el sistema de créditos

Se recomienda introducir primero los conceptos de capital, tasa, plazo e cuota. Luego explicar cómo interactúan entre sí.

## 10.8 Cómo explicar la fórmula francesa

La explicación debe ser visual y gradual. Es útil mostrar:

- qué representa la tasa mensual;
- cómo se obtiene la cuota fija;
- cómo cambia la proporción entre interés y capital.

## 10.9 Cómo explicar el redondeo

Este punto es muy valioso porque demuestra madurez técnica. Se puede explicar que los sistemas financieros no pueden perder centavos por redondeo excesivo y que es necesario ajustar la última cuota o acumular el residuo.

## 10.10 Cómo explicar el cálculo de fechas

Se debe enfatizar que la fecha de vencimiento se calcula a partir de la fecha de desembolso y que si cae en domingo, se corrige al siguiente día hábil.

## 10.11 Preguntas que puede hacer el profesor

### Pregunta 1
¿Por qué usar un ORM en lugar de escribir SQL directamente?

Respuesta recomendada:
Porque mejora la productividad, evita errores manuales y permite trabajar con un modelo orientado a objetos.

### Pregunta 2
¿Por qué la lógica no debe ir en la vista?

Respuesta recomendada:
Porque la vista debe limitarse a presentar datos; la lógica de negocio pertenece al controlador o al modelo.

### Pregunta 3
¿Por qué las cuotas deben ajustarse en el redondeo?

Respuesta recomendada:
Porque los montos financieros necesitan exactitud, y los errores acumulados pueden alterar el saldo final del crédito.

### Pregunta 4
¿Por qué se mueve la fecha si cae domingo?

Respuesta recomendada:
Porque se busca que el vencimiento sea un día hábil, lo cual es una práctica común en la operación financiera.

## 10.12 Errores comunes durante la exposición

- explicar el ORM como magia sin mostrar su funcionamiento real;
- mezclar lógica de negocio con la vista;
- mostrar la fórmula francesa sin explicar el significado de sus variables;
- omitir la importancia del redondeo y del ajuste final;
- presentar la base de datos como un detalle secundario cuando en realidad es central.

## 10.13 Recomendaciones para una presentación profesional

- usar ejemplos concretos;
- mostrar el flujo del sistema con diagramas sencillos;
- destacar la relación entre el código y la operación financiera real;
- demostrar que el sistema no solo es funcional, sino también técnico y bien estructurado;
- hablar con seguridad, pero sin perder claridad pedagógica.

---

## Conclusiones

El proyecto desarrollado representa una aplicación web funcional, educativa y tecnológicamente sólida para la gestión de préstamos. Su diseño combina un framework ligero como Flask con un ORM robusto como SQLAlchemy, lo que permite separar responsabilidades, organizar el código y simplificar el acceso a los datos. La arquitectura usada facilita la comprensión de conceptos fundamentales de ingeniería de software, como separación de capas, manejo de datos, lógica de negocio y presentación.

En el contexto académico, el sistema no solo demuestra la capacidad de construir una aplicación operativa, sino también la posibilidad de explicar conceptos técnicos complejos con una base práctica. La implementación de amortización, manejo de cuotas, control de fechas y persistencia de datos permiten conectar teoría financiera con la programación aplicada.

## Recomendaciones

1. Mantener la separación entre lógica de negocio y vistas.
2. Continuar usando un ORM para simplificar las operaciones de persistencia.
3. Probar rigurosamente el cálculo de cuotas y el ajuste final de centavos.
4. Documentar la lógica financiera para que sea comprensible desde el punto de vista técnico y académico.
5. Considerar la incorporación de migraciones más formales y pruebas automatizadas en futuras versiones.
6. Extender el sistema con seguridad, autenticación, roles de usuario y reportes más completos.
7. Mantener una estructura modular para facilitar el crecimiento del proyecto.

---

## Referencias conceptuales del proyecto

- [app.py](app.py): punto de entrada de la aplicación Flask.
- [database.py](database.py): configuración y conexión con la base de datos.
- [models.py](models.py): entidades del dominio y lógica financiera.
- [templates/base.html](templates/base.html): layout base de la interfaz.
- [templates/dashboard.html](templates/dashboard.html): vista principal del sistema.
- [requirements.txt](requirements.txt): dependencias del proyecto.
