import os
from dotenv import load_dotenv
from os import environ

# Cargar variables de entorno desde el archivo .env
load_dotenv()


class Config(object):
    """BaseConfiguration."""
    SECRET_KEY = "proyecto2024"
    TESTING = False
    SESSION_TYPE = "filesystem"

class ProductionConfig(Config):
    """Production configuration."""
    MINIO_SERVER = environ.get("MINIO_SERVER")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY")
    MINIO_SECURE = True
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")


class DevelopmentConfig(Config):
    """Development configuration."""
    # Agrego variables de entorno (junto con algunos valores default por si no las encuentra)
    MINIO_SERVER = os.getenv("MINIO_SERVER_DEV", "127.0.0.1:9000")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY_DEV")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_DEV")
    MINIO_SECURE = False

    DB_USER = os.getenv("DB_USER_DEV", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD_DEV", "postgres")
    DB_HOST = os.getenv("DB_HOST_DEV", "localhost")
    DB_PORT = os.getenv("DB_PORT_DEV", "5432")
    DB_NAME = os.getenv("DB_NAME_DEV", "grupo28")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = False

config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "test": TestingConfig
}