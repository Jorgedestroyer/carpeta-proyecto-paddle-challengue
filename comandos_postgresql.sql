# COMANDOS PARA CREAR LA BASE DE DATOS
# Ejecutar en SQL Shell (psql) después de instalar PostgreSQL 18

# 1. Abrir SQL Shell (psql)
# 2. Presionar Enter para todos los valores por defecto
# 3. Introducir la contraseña del superusuario postgres
# 4. Ejecutar estos comandos uno por uno:

CREATE DATABASE paddle_challenge_db;
CREATE USER paddle_user WITH PASSWORD 'paddle123';
GRANT ALL PRIVILEGES ON DATABASE paddle_challenge_db TO paddle_user;

# 5. Salir
\q