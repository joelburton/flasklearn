"""Flask application configurations."""

import datetime
import os
import tempfile


class Config(object):
    """Base configuration."""

    SECRET_KEY = 'supersecret'

    RECAPTCHA_PUBLIC_KEY = "6LfZ6g8TAAAAAD6_hj6otG-A5UHK-g2A1hUXSIMU"
    RECAPTCHA_PRIVATE_KEY = "6LfZ6g8TAAAAANxemwLq2YQ6vXdGerLNjHPSiMVe"

    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_PANELS = [
        'flask_debugtoolbar.panels.versions.VersionDebugPanel',
        'flask_debugtoolbar.panels.timer.TimerDebugPanel',
        'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
        'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
        'flask_debugtoolbar.panels.config_vars.ConfigVarsDebugPanel',
        'flask_debugtoolbar.panels.template.TemplateDebugPanel',
        'flask_debugtoolbar.panels.logger.LoggingPanel',
        'flask_debugtoolbar.panels.route_list.RouteListDebugPanel',
        'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
        'flask.ext.mongoengine.panels.MongoDebugPanel',
        'flask_debugtoolbar.panels.sqlalchemy.SQLAlchemyDebugPanel',
    ]


    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MONGODB_SETTINGS = {
        'db': 'local',
        'host': 'localhost',
        'port': 27017
    }

    CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"
    CELERY_RESULT_BACKEND = "amqp://guest:guest@localhost:5672//"

    CELERYBEAT_SCHEDULE = {
        'log-every-30-seconds': {
            'task': 'blogapp.tasks.log',
            'schedule': datetime.timedelta(seconds=30),
            'args': ("Message",)
        },
    }

    # don't compile flask-assets assets
    ASSETS_DEBUG = True

    MAIL_SERVER = 'email-smtp.us-east-1.amazonaws.com'
    MAIL_USERNAME = 'AKIAIDQJEDLNTSM73G7A'
    MAIL_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'FIXME')
    MAIL_USE_TLS = True

    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/flasklearn"

    CACHE_TYPE = 'simple'


class ProdConfig(Config):
    """Production configuration."""

    ASSETS_DEBUG = False
    DEBUG = False
    SQLALCHEMY_ECHO = False


class DevConfig(Config):
    """Development configuration."""


class TestConfig(Config):
    """Testing configuration."""

    db_file = tempfile.NamedTemporaryFile()

    DEBUG_TB_ENABLED = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_file.name

    CACHE_TYPE = 'null'
    WTF_CSRF_ENABLED = False

