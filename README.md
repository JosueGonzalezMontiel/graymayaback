# API Tienda de Ropa

Esta API está construida con **FastAPI** y **Peewee** sobre **MySQL** para servir como
backend de una tienda de ropa. El diseño de la base de datos sigue los
requerimientos expuestos en el documento adjunto y está normalizado
hasta tercera forma normal. La arquitectura está inspirada en el
repositorio original `tep`, reutilizando patrones como la separación
entre modelos, esquemas Pydantic, repositorios y rutas.

## Estructura del proyecto

```
clothing_api/
│
├── app/
│   ├── api/
│   │   ├── deps.py          # Dependencias comunes (API Key)
│   │   └── routers/        # Rutas agrupadas por recurso
│   │       ├── categorias.py
│   │       ├── tallas.py
│   │       ├── patrones.py
│   │       ├── colaboradores.py
│   │       ├── clientes.py
│   │       ├── productos.py
│   │       ├── pedidos.py
│   │       └── insumos.py
│   ├── core/
│   │   └── config.py        # Configuración de la aplicación y variables de entorno
│   ├── db/
│   │   └── peewee_conn.py   # Conexión a la base de datos y utilidades
│   ├── models/              # Modelos Peewee correspondientes a cada tabla
│   ├── repositories/        # Operaciones CRUD encapsuladas
│   ├── schemas/             # Esquemas Pydantic para validar entradas y salidas
│   └── main.py              # Punto de entrada de la API
├── requirements.txt         # Dependencias Python
└── README.md                # Este documento
```

## Configuración

Antes de ejecutar la API asegúrate de tener un servidor MySQL en
ejecución y crea una base de datos vacía (por defecto se llama
`tienda_ropa`). Puedes configurar los parámetros de conexión mediante
variables de entorno:

- `DB_NAME`: nombre de la base de datos (por defecto `tienda_ropa`)
- `DB_USER`: usuario de MySQL
- `DB_PASSWORD`: contraseña de MySQL
- `DB_HOST`: host de la base de datos (por defecto `localhost`)
- `DB_PORT`: puerto de la base de datos (por defecto `3306`)
- `API_KEY`: clave de API para proteger las rutas (opcional)

En entornos de desarrollo puedes crear un entorno virtual e instalar
las dependencias con:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

Para iniciar la aplicación en desarrollo puedes usar `uvicorn`:

```bash
uvicorn app.main:app --reload
```

Al iniciar, la aplicación creará automáticamente las tablas de la base
de datos si no existen. Las rutas estarán disponibles en
`http://localhost:8000` por defecto.
