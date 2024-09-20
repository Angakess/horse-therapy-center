class Config(object):
    """BaseConfiguration."""

    SECRET_KEY = "secret"
    TESTING = False
    SESSION_TYPE = "filesystem"

class ProductionConfig(Config):
    """Production configuration."""
    pass

class DevelopmentConfig(Config):
    """Development configuration."""
    pass

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = False

config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "test": TestingConfig
}