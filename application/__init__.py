import logging
import os

import redis
from dotenv import load_dotenv
from flask import Flask

from .data_loader import load_data
from .gallery_loader import GalleryLoader
from .github_client import GithubClient
from .routes import MAIN_BLUEPRINT

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


def create_redis_client() -> redis.client.Redis:
    try:
        client: redis.client.Redis = redis.from_url(os.getenv("REDIS_URL"))
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
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 86400

    # Redis client creation for caching
    redis_client = create_redis_client()
    # GitHub client for getting the gallery images
    git_hub_client = GithubClient(os.environ["GITHUB_USERNAME"], os.environ["GITHUB_TOKEN"])
    # Helper class to load gallery images on-demand
    gallery_loader_obj = GalleryLoader(redis_client, git_hub_client)

    # Create the data dictionary and add it to the app config for access by the blueprints
    app.config["data"] = load_data()
    app.config["gallery_loader"] = gallery_loader_obj

    # Register blueprints to add routes to the app
    app.register_blueprint(MAIN_BLUEPRINT, url_prefix="/")

    return app
