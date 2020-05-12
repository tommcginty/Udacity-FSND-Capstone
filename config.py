import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """This is the parent configuration class."""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    
class StagingConfig(Config):
    """Configurations for Staging."""
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TESTDB_URL')



