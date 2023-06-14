from flask import Flask


def create_app():
    app = Flask(__name__)

    from .browse import browse
    from .detail import detail
    from .search import search

    app.register_blueprint(browse, prefix='/')
    app.register_blueprint(detail, prefix='/')
    app.register_blueprint(search, prefix='/')

    return app
