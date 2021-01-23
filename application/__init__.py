import logging

from flask import Flask, request, redirect

from .routes import MAIN_BLUEPRINT
from .data_loader import load_data

application = Flask(__name__)

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


def create_flask_app() -> Flask:
    # Create the flask app
    app = Flask(__name__)

    # Create the data dictionary and add it to the app config for access by the blueprints
    app.config["data"] = load_data()

    _setup_app(application)

    # Register blueprints to add routes to the app
    app.register_blueprint(MAIN_BLUEPRINT, url_prefix="/")

    return app


def _setup_app(app):
    @app.before_request
    def before_request():
        # Redirect to HTTPS automatically
        if request.url.startswith("http://"):
            url = request.url.replace("http://", "https://", 1)
            code = 301
            return redirect(url, code=code)
