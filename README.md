






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


