from flask import Flask


def create_app():
    app = Flask(__name__)

    from .browse import browse
    from .detail import detail

    app.register_blueprint(browse, prefix='/')
    app.register_blueprint(detail, prefix='/')

    return app
