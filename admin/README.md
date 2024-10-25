# Trabajo Integrador (TI) - Etapa 1
Esta aplicación permitirá la administración de altas, bajas y modificaciones de los recursos necesarios para el sistema, ademas de habilitar  un registro de usuarios y un sistema de autenticación para operar con la aplicación. Será utilizada tanto por los administradores del sistema que tienen el acceso a la administración de los usuarios, como también los distintos usuarios con roles delimitados según el área correspondiente.

## Funcionalidad de la aplicación
* Mantener un registro histórico de los legajos de los J&A (Jinetes y Amazonas), incluyendo anexos de documentación necesaria.
* Mantener un registro de los Legajos de los profesionales del equipo.
* Mantener un registro de los cobros y pagos realizados.
* Registrar la información de los caballos.

## Dependencias principales
* python v3.12.3
* flask v3.0.3
* pytest v8.3.3
* psycopg2-binary v2.9.9
* flask-sqlalchemy v3.1.1
* flask-session v0.8.0
* flask-bcrypt v1.0.1
* minio v7.2.9
* python-dotenv v1.0.1

## Instalación y ejecución
Este proyecto utiliza Poetry para la gestión de dependencias y el entorno virtual. A continuación, se describe el proceso de instalación y configuración.

#### 1. Clonar el repositorio
Primero, clona el repositorio en tu máquina local:
``` bash
git clone git@gitlab.catedras.linti.unlp.edu.ar:proyecto2024/proyectos/grupo28/code.git
cd admin
```

#### 2. Instalar Poetry
Si aún no tienes Poetry instalado, puedes instalarlo ejecutando el siguiente comando (asegúrate de tener Python previamente instalado):
``` bash
curl -sSL https://install.python-poetry.org | python3 -
```

#### 3. Configurar el entorno virtual e instalar dependencias
Poetry se encargará de crear el entorno virtual y de instalar todas las dependencias necesarias:
```bash
poetry install
```
Este comando instala las dependencias listadas en el archivo pyproject.toml y prepara el entorno virtual en el proyecto.

#### 4. Activar el entorno virtual
Para activar el entorno virtual gestionado por Poetry, puedes utilizar:
``` bash
poetry shell
```
Si no quieres activar el entorno virtual, puedes ejecutar comandos dentro de él de esta manera:

#### 5. Variables de entorno
El proyecto requiere de variables de entorno a la hora de configurar la conexión con la base de datos y el servidor de MinIO, ya sea para producción o desarrollo. Para realizar la configuración de desarrollo deberá crearlas en un archivo `.env` dentro de la carpeta `src/` y definir las siguientes variables:
```
# Configuración de la base de datos
DB_USER_DEV=<tu_usuario>
DB_PASSWORD_DEV=<tu_contraseña>
DB_HOST_DEV=<host_de_tu_bd>
DB_PORT_DEV=<puerto_de_tu_bd>
DB_NAME_DEV=<nombre_de_tu_bd>

# Configuración del servidor MinIO
MINIO_SERVER_DEV=<host_de_minio:puerto>
MINIO_ACCESS_KEY_DEV=<tu_access_key>
MINIO_SECRET_DEV=<tu_secret_key>
``` 
Para la configuracion de produccion deberá crear las variables de entorno dentro de [Vault](https://vault.proyecto2024.linti.unlp.edu.ar/ui/vault/auth?with=oidc) con los siguienes nombres:
```
# Configuración de la base de datos (debe estar dentro de una carpeta 'database')
URL=<url_de_tu_bd>

# Configuración del servidor MinIO (debe estar dentro de una carpeta 'minio')
SERVER=<url_de_minio>
ACCESS_KEY=<tu_access_key>
SECRET=<tu_secret_key>
``` 
> **Nota:** Reemplaza <tu_usuario>, <host_de_tu_bd>, <puerto_de_tu_bd>, y otros valores de ejemplo por los detalles de tu propia configuración. Para más información, consulta la [documentación de PostgreSQL](https://www.postgresql.org/docs/) y la [documentación de MinIO](https://min.io/docs/minio/kubernetes/upstream/).

#### 6. Ejecución de la aplicación
Para ejecutar la aplicación, utiliza el siguiente comando en la raíz del proyecto:
``` bash
flask run
```
Este comando iniciará la aplicación en modo estándar. Si necesitas habilitar el modo de depuración para ver mensajes detallados y facilitar la detección de errores durante el desarrollo, puedes utilizar:

``` bash
flask run --debug
```

## Usuarios de Prueba

| Alias         | Email                         | Contraseña          | Rol         |
|---------------|-------------------------------|---------------------|-------------|
| Admin         | admin@example.com             | adminpassword       | SystemAdmin |
| AnaVoluntaria | ana.voluntaria@example.com    | voluntariopassword1 | Voluntario  |
| CarlosGomez   | carlos.gomez@example.com      | password2           | Técnico     |
| MarcosZ       | marcos.zapata@example.com     | passwordMarcos      | Admin       |
| Rocky         | ryland.grace@hailmary.com     | astrofagos          | Ecuestre    |

## Contribuyentes

* Agustina Cabello
* Augusto Conti
* Matias Cuacci
* Andrés Gabriel Kessler