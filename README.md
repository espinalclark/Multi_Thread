| / () || () || () || | | | | | | | |
| \ / | | | | | | | | | || || || |
||/|||_||_||_||__|_____/
Multi_Thread — Descargas segmentadas, resilientes y automáticas


> Minimalista. Robusto. Diseñado para romper límites de ancho de banda — no para romper reglas.

---

## ⚡ Descripción

**Multi_Thread** es un proyecto de descargas multihilo pensado para optimizar la velocidad y confiabilidad de transferencias.  
Combina potencia de concurrencia, reanudación automática y autenticación integrada.

Ideal para:
- Descargas masivas.
- Scripts automatizados.
- Pruebas de red controladas.
- Aplicaciones seguras con gestión de usuarios.

---

## 🗂️ Estructura del proyecto

.
├── Multi_Thread.sql # Estructura / dump de base de datos MariaDB
├── README.md
├── auth/ # Lógica de autenticación y registro
│ ├── login.py
│ ├── password_utils.py
│ ├── register.py
│ └── user_manager.py
├── database.py # Conexión con MariaDB
├── downloader.py # Núcleo de descargas multihilo
├── downloads/ # Carpeta donde se almacenan los archivos descargados
├── essets/itachi.jpg # Imagen decorativa (se recomienda renombrar a 'assets/')
├── generate_hashes.py # Generador de hashes (bcrypt)
├── main.py # Punto de entrada principal
├── requirements.txt # Dependencias del proyecto
├── run.sh # Script de ejecución rápida
├── test_db.py # Test de conexión con la base de datos
├── threads/segment_thread.py # Gestión individual de segmentos de descarga
├── ui/ # Interfaz gráfica (login, dashboard, widgets)
│ ├── app.py
│ ├── dashboard.py
│ ├── login_window.py
│ └── widgets.py
└── utils/ # Utilidades generales (configuración, logs, helpers)
├── config.py
├── helpers.py
└── logger.py


> `xd.txt` se usa temporalmente para levantar el servidor durante instalación.

---

## ⚙️ Requisitos

- Python **3.10+**
- MariaDB / MySQL
- Linux (probado en Arch, Kali, Archcraft)
- pip y virtualenv

Instala dependencias:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

Configuración de base de datos
- importar el archivo SQL: 
mysql -u root -p multi_thread_db < Multi_Thread.sql

- configuracion en utils/config.py
DB_NAME=multi_thread_db
DB_USER=tu_usuario
DB_PASS=tu_contraseña
DB_HOST=localhost
DB_PORT=3306

Ejecución
Opción 1 — Script automático

chmod +x run.sh
./run.sh

Opción 2 — Manual

source .venv/bin/activate
python main.py

Autor

cl4rksec
Entusiasta del pentesting.

Repositorio oficial: https://github.com/espinalclark/Multi_Thread
