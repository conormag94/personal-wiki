from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    app_settings = 'project.config.DevelopmentConfig'
    app.config.from_object(app_settings)

    db.init_app(app)

    from project.routes import wiki
    app.register_blueprint(wiki)

    return app