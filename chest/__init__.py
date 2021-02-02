"""Main application package."""

import os
from flask import Flask, request, abort

from . import db, index, dictionary

def create_app(test_config=False):
    """ application factory function"""
    app = Flask(__name__)

    if test_config:
        app.config.from_pyfile('../configs/test_settings.cfg')
    else:
        app.config.from_pyfile('../configs/settings.cfg')

    db.init_app(app)

    app.register_blueprint(index.bp)
    app.register_blueprint(dictionary.bp)

    return app
