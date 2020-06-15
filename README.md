# koimetrics-website

# Proyecto: Gestion de polizas

## Instalacion en entorno linux (basado en Debian)


#### Creacion base de datos (PostgreSQL)

Instalacion de dependencias:
```
sudo apt-get update
sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib
```

Crear base de datos y usuario
```
sudo -u postgres psql
postgres=# CREATE DATABASE koimetrics_db;
CREATE DATABASE
postgres=# CREATE USER  koimetrics_db_user WITH PASSWORD '< password >';
CREATE ROLE
```

Suministrar permisos al usuario de la base de datos
```
postgres=# ALTER ROLE koimetrics_db_user SET client_encoding TO 'utf8';
ALTER ROLE
postgres=# ALTER ROLE koimetrics_db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE
postgres=# ALTER ROLE koimetrics_db_user SET timezone TO 'UTC';
ALTER ROLE
postgres=# GRANT ALL PRIVILEGES ON DATABASE koimetrics_db TO koimetrics_db_user;
GRANT
postgres=# ALTER USER koimetrics_db_user CREATEDB;
ALTER ROLE
postgres=# \q
```
Luego de esto, configurar el valor DB_PASSWORD en el archivo .env con el mismo valor proporcionado en < password > al crear el usuario de la base de datos.
