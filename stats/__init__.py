from flask import Flask, jsonify

from stats import db


class BadRequest(Exception):
    """Raise to return a 400"""
    def __init__(self, message):
        super().__init__()
        self.message = message


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    from . import api
    app.register_blueprint(api.bp)

    from . import web
    app.register_blueprint(web.bp)

    db.init(app)

    from . import models

    # Set up a handler for our custom exception class
    @app.errorhandler(BadRequest)
    def handle_invalid_usage(error):
        response = jsonify(dict(message=error.message))
        response.status_code = 400
        return response

    return app
