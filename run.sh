#!/bin/bash
# ─────────────────────────────────────────────────────────────
# Script de inicialización automática para el proyecto Multi_Thread
# Autor: cl4rksec
# Descripción: Configura el entorno, instala dependencias y ejecuta el proyecto.
# ─────────────────────────────────────────────────────────────

# --- Variables ---
PROJECT_DIR="$HOME/Cybersecurity/Scripts/Multi_Thread"
VENV_DIR="$PROJECT_DIR/venv"
REQ_FILE="$PROJECT_DIR/requirements.txt"
DB_NAME="Multi_Thread"

# --- Colores ---
GREEN="\e[32m"
RED="\e[31m"
YELLOW="\e[33m"
RESET="\e[0m"

echo -e "${GREEN}Iniciando configuración del proyecto Multi_Thread...${RESET}"

# --- Verificar si el directorio del proyecto existe ---
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED} No se encontró el directorio del proyecto: $PROJECT_DIR${RESET}"
    exit 1
fi

cd "$PROJECT_DIR" || exit

# --- Crear entorno virtual si no existe ---
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Creando entorno virtual...${RESET}"
    python -m venv venv
else
    echo -e "${GREEN}Entorno virtual encontrado.${RESET}"
fi

# --- Activar entorno virtual ---
source "$VENV_DIR/bin/activate"

# --- Instalar dependencias ---
if [ -f "$REQ_FILE" ]; then
    echo -e "${YELLOW}Instalando dependencias desde requirements.txt...${RESET}"
    pip install --upgrade pip
    pip install -r "$REQ_FILE"
else
    echo -e "${RED}No se encontró requirements.txt${RESET}"
fi

# --- Verificar MariaDB ---
echo -e "${YELLOW} Verificando servicio MariaDB...${RESET}"
if ! systemctl is-active --quiet mariadb; then
    echo -e "${YELLOW} MariaDB no está activo. Iniciando servicio...${RESET}"
    sudo systemctl start mariadb
else
    echo -e "${GREEN}MariaDB está corriendo.${RESET}"
fi

# --- Verificar base de datos ---
echo -e "${YELLOW}🗄️ Verificando base de datos '$DB_NAME'...${RESET}"
DB_EXISTS=$(sudo mariadb -u root -e "SHOW DATABASES LIKE '$DB_NAME';" | grep "$DB_NAME")

if [ -z "$DB_EXISTS" ]; then
    echo -e "${YELLOW} Creando base de datos $DB_NAME...${RESET}"
    sudo mariadb -u root -e "CREATE DATABASE $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
else
    echo -e "${GREEN} Base de datos $DB_NAME existente.${RESET}"
fi

# --- Ejecutar proyecto ---
echo -e "${GREEN} Ejecutando proyecto...${RESET}"
python main.py

