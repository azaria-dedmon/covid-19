import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(16)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    WTF_CSRF_ENABLED = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """Configurations for Development Environment."""

    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE') or 'postgresql:///covid'

class TestingConfig(Config):
    """Configurations for Testing Environment."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE') or 'postgresql:///covidtest'

class ProductionConfig(Config):
    """Configurations for Production Environment."""
    ENV = 'production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('HEROKU_POSTGRESQL_YELLOW_URL')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 