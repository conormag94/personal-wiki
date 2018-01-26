import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    DEBUG = True
    VERIFY_WEBHOOKS = False
    
    # Config variables
    SECRET_KEY = os.environ.get('SECRET_KEY')
    GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME')
    GITHUB_API_KEY = os.environ.get('GITHUB_API_KEY')