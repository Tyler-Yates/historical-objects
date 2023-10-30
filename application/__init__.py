import logging
import os

import redis
from dotenv import load_dotenv
from flask import Flask, request, redirect

from .github_client import GithubClient
from .routes import MAIN_BLUEPRINT
from .data_loader import load_data

application = Flask(__name__)

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


def create_redis_client() -> redis.client.Redis:
    try:
        client = redis.from_url(os.getenv("REDIS_URL"))
        ping = client.ping()
        if ping is True:
            return client
    except redis.AuthenticationError as e:
        print("AuthenticationError connecting to Redis")
        raise e


def create_flask_app() -> Flask:
    # Load the environment variables from the .env file
    load_dotenv()

    # Create the flask app
    app = Flask(__name__)

    # Set the default cache control headers on static elements
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 86400

    # Redis client creation for caching
    redis_client = create_redis_client()

    git_hub_client = GithubClient(os.environ["GITHUB_USERNAME"], os.environ["GITHUB_TOKEN"])

    # Create the data dictionary and add it to the app config for access by the blueprints
    app.config["data"] = load_data(redis_client, git_hub_client)

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
