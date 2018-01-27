import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class BaseConfig:
    DEBUG = False
    TESTING = False
    VERIFY_WEBHOOKS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Config variables
    SECRET_KEY = os.environ.get('SECRET_KEY')
    GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME')
    GITHUB_API_KEY = os.environ.get('GITHUB_API_KEY')

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db', 'wiki.db')

class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db', 'wiki-test.db')

class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    VERIFY_WEBHOOKS = True