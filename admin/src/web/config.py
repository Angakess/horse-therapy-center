class Config(object):
    """BaseConfiguration."""

    SECRET_KEY = "proyecto2024"
    TESTING = False
    SESSION_TYPE = "filesystem"

class ProductionConfig(Config):
    """Production configuration."""
    pass

class DevelopmentConfig(Config):
    """Development configuration."""
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "grupo28"
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