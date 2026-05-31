# Gestor de Egresos - Flask

Aplicación web desarrollada en Flask 

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para clonar el repositorio)

## Instalación

### 1. Clonar o descargar el proyecto

```bash
git clone <url-del-repositorio>
cd pflask23
```

### 2. Crear un entorno virtual

**En Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Configuración

### Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
SECRET_KEY=tu-clave-secreta-aqui
DATABASE_URL=sqlite:///egreso.db
FLASK_ENV=development
```

**Nota:** Si no se especifica `DATABASE_URL`, la aplicación usará SQLite por defecto (`egreso.db`).

Para usar PostgreSQL, configura:
```env
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_base_datos
```

## Ejecución

### Opción 1: Modo Desarrollo (Recomendado)

```bash
flask run
```

La aplicación estará disponible en: `http://localhost:5000`

### Opción 2: Con Gunicorn (Producción)

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

La aplicación estará disponible en: `http://localhost:8000`

## Estructura del Proyecto

```
pflask23/
├── app.py              # Aplicación principal y rutas
├── config.py           # Configuración de la aplicación
├── models.py           # Modelos de base de datos (Egreso, FormaPago)
├── requirements.txt    # Dependencias del proyecto
├── static/
│   └── css/
│       └── style.css   # Estilos CSS
└── templates/
    ├── abase.html      # Plantilla base
    ├── index.html      # Página principal
    ├── crear.html      # Formulario crear egreso
    ├── editar.html     # Formulario editar egreso
    └── buscar.html     # Página de búsqueda
```

## Funcionalidades

- ✅ Crear nuevos egresos
- ✅ Editar egresos existentes
- ✅ Eliminar egresos
- ✅ Listar todos los egresos
- ✅ Buscar egresos
- ✅ Registrar forma de pago (Efectivo, Tarjeta Débito, Tarjeta Crédito, Transferencia)

## Troubleshooting

### Error: "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Error: "Base de datos no existe"
La aplicación creará automáticamente la base de datos al iniciar. Si usas PostgreSQL, asegúrate de que el servidor esté corriendo.

### Puerto 5000 ya está en uso
```bash
flask run --port 5001
```

## Desarrollo

Para realizar cambios en el código:

1. Asegurate que el entorno virtual esté activado
2. Realiza tus cambios
3. El servidor de desarrollo recargará automáticamente los cambios
4. Prueba la aplicación en tu navegador

## Desactivar el Entorno Virtual

```bash
deactivate
```

## Licencia

Este proyecto es de uso educativo.
