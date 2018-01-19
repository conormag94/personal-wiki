from flask import Flask

from .config import Config

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    from project.routes import wiki
    app.register_blueprint(wiki)

    return app