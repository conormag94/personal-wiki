import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class BaseConfig:
    DEBUG = False
    TESTING = False
    VERIFY_WEBHOOKS = False
    
    # Config variables
    SECRET_KEY = os.environ.get('SECRET_KEY')
    GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME')
    GITHUB_API_KEY = os.environ.get('GITHUB_API_KEY')

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True

class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    VERIFY_WEBHOOKS = True