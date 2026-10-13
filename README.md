# PoliRestaurante API 🍽️

Sistema backend para la gestión de restaurante con FastAPI, SQLModel y PostgreSQL.

## 🚀 Requisitos Previos

- Python 3.10+
- PostgreSQL en ejecución (puerto 5432)
- Base de datos creada: `polirestaurante`

## 📦 Instalación

1. **Crear y activar entorno virtual**:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. **Instalar dependencias**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Configurar base de datos**:
   Copia el archivo `.env.example` a `.env` y coloca tu contraseña:
   ```powershell
   cp .env.example .env
   ```
   O configura la variable de entorno:
   ```powershell
   $env:DATABASE_URL = "postgresql+psycopg2://postgres:TU_PASSWORD@127.0.0.1:5432/polirestaurante"
   ```

## ▶️ Ejecución del Servidor

```powershell
python -m uvicorn main:app --reload
```

## 🌐 Endpoints y Documentación

- **Frontend / Vista Web:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Documentación Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Documentación ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 📁 Estructura del Proyecto

```text
pyt_web/
├── .env.example         # Plantilla de variables de entorno
├── .gitignore           # Archivos ignorados por Git
├── requirements.txt     # Dependencias del proyecto
├── README.md            # Documentación del proyecto
├── main.py              # Punto de entrada FastAPI
├── DataBase.py          # Conexión y sesión de base de datos
├── models/              # Modelos de SQLModel (User, Table, Product, etc.)
├── routers/             # Rutas por rol (admin, cocina, mesero)
├── static/              # Frontend web (HTML, CSS, JS)
├── crud_driver.py       # Script CRUD con SQL puro
├── crud_orm.py          # Script CRUD con ORM
└── postman/             # Colecciones de pruebas API
```
