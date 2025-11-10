# Multi_Thread

**Descargas segmentadas, resilientes y automáticas**

> Minimalista. Robusto. Diseñado para exprimir el ancho de banda, no para romper reglas.

---

##  Resumen

Multi_Thread es un gestor de descargas multihilo pensado para maximizar velocidad y fiabilidad en transferencias de archivos.
Ofrece concurrencia por segmentos, reanudación automática, control de errores y autenticación integrada para uso en scripts y aplicaciones seguras.

Perfecto para:

* Descargas masivas y paralelas.
* Scripts de automatización y pipelines.
* Pruebas de rendimiento y redes.
* Integración en aplicaciones con gestión de usuarios.

---

##  Estructura del proyecto

```
.
├── Multi_Thread.sql            # Dump / estructura de la base de datos (MariaDB/MySQL)
├── README.md
├── auth/                       # Lógica de autenticación y registro
│   ├── login.py
│   ├── password_utils.py
│   ├── register.py
│   └── user_manager.py
├── database.py                 # Conexión con MariaDB
├── downloader.py               # Núcleo: descargas multihilo y segmentadas
├── downloads/                  # Archivos descargados
├── assets/itachi.jpg           # Recursos (renombrado desde "essets/")
├── generate_hashes.py          # Generador de hashes (bcrypt)
├── main.py                     # Punto de entrada
├── requirements.txt            # Dependencias
├── run.sh                      # Script de ejecución rápida
├── test_db.py                  # Test de conexión a la DB
├── threads/segment_thread.py   # Gestión de cada segmento de descarga
├── ui/                         # Interfaz (login, dashboard, widgets)
│   ├── app.py
│   ├── dashboard.py
│   ├── login_window.py
│   └── widgets.py
└── utils/                      # Utilidades (configuración, logs, helpers)
    ├── config.py
    ├── helpers.py
    └── logger.py
```

> Nota: `xd.txt` se utiliza temporalmente durante la instalación para levantar el servidor. Eliminar o reemplazar antes de producción.

---

## Requisitos

* Python **3.10+**
* MariaDB / MySQL
* Linux (probado en Arch, Kali, Archcraft)
* pip y virtualenv

---

## Instalación rápida

1. Crear y activar entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Configurar la base de datos (MariaDB/MySQL):

```bash
# Crear la base de datos y cargar el dump
mysql -u root -p < Multi_Thread.sql
# (o) mysql -u root -p multi_thread_db < Multi_Thread.sql
```

3. Actualizar `utils/config.py` con las credenciales:

```py
DB_NAME = "multi_thread_db"
DB_USER = "tu_usuario"
DB_PASS = "tu_contraseña"
DB_HOST = "localhost"
DB_PORT = 3306
```

---

## Ejecución

**Opción 1 — Script automático**

```bash
chmod +x run.sh
./run.sh
```

**Opción 2 — Manual (recomendado para desarrollo)**

```bash
source .venv/bin/activate
python main.py
```

---

## Tests y diagnóstico

* `test_db.py`: prueba de conexión y validación de tablas.
* Logs: revisar `utils/logger.py` y la carpeta de logs configurada.

---

## Buenas prácticas / Seguridad

* No almacenar credenciales en texto plano: usar variables de entorno o un archivo `.env` fuera del repositorio.
* Revisar y rotar claves con regularidad.
* Limitar permisos del usuario de la base de datos.
* Revisar la carpeta `downloads/` para evitar sobreescrituras inesperadas.

---

## Contribución

1. Fork del repo
2. Crear branch: `feature/mi-mejora`
3. Commit y PR explicando el cambio

---

##  Autor

**cl4rksec** — Entusiasta del pentesting

Repositorio oficial: `https://github.com/espinalclark/Multi_Thread`

---

