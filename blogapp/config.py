"""Flask application configurations."""


class Config(object):
    pass


class ProdConfig(Config):
    pass


class DevConfig(Config):
    """Development configuration."""

    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/flasklearn"
    SECRET_KEY = 'supersecret'
