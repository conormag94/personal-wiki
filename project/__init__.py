from flask import Flask

def create_app():

    app = Flask(__name__)

    app_settings = 'project.config.DevelopmentConfig'
    app.config.from_object(app_settings)

    from project.routes import wiki
    app.register_blueprint(wiki)

    return app