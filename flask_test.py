from flask import Flask
from app.api.v1 import v1
from app.core.models import db_wrapper
from config import config
from app.core.utils.response import JsonResponse
from app.core.utils.mongodb import mongo


def create_app(config_name='default'):

    app = Flask(__name__)
    app.response_class = JsonResponse
    try:
        app.config.from_object(config[config_name])
    except KeyError:
        app.config.from_object(config['default'])
    db_wrapper.init_app(app)
    mongo.init_app(app)
    app.register_blueprint(v1, url_prefix='/api/v1')

    return app

application = create_app()


if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix
    application.wsgi_app = ProxyFix(application.wsgi_app)
    application.run()
