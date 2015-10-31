"""Flask application configurations."""


class Config(object):
    """Base configuration."""

    RECAPTCHA_PUBLIC_KEY="6LfZ6g8TAAAAAD6_hj6otG-A5UHK-g2A1hUXSIMU"
    RECAPTCHA_PRIVATE_KEY="6LfZ6g8TAAAAANxemwLq2YQ6vXdGerLNjHPSiMVe"


class ProdConfig(Config):
    pass


class DevConfig(Config):
    """Development configuration."""

    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/flasklearn"
    SECRET_KEY = 'supersecret'
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
