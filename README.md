[![tox](https://github.com/Tyler-Yates/historical-objects/actions/workflows/tox-workflow.yml/badge.svg)](https://github.com/Tyler-Yates/historical-objects/actions/workflows/tox-workflow.yml)

# historical-objects

This website is currently hosted at https://historical-objects.onrender.com/

## Prerequisites
This README assumes you are running on Linux.

You will need a [Python 3](https://www.python.org/about/) interpreter to run this application.
The Python 3 interpreter should include the `venv` module.
The recommended Python version for this project will be specified in the config on render.com.

You will need a Redis instance for caching.

## Setup

### Python
You will need to create a virtual environment to run this application.
Run the following commands at the root of this repo:
```
python3 -m venv venv
source venv/bin/activate
pip install -Ur requirements.txt
```

### Environment
You will need to set the following environment variables:
```
REDIS_URL = URL for Redis instance to cache things
GITHUB_USERNAME = username for GitHub API access
GITHUB_TOKEN = personal access token for GitHub API access
```

You can copy the `.env.example` file to simplify this.

## Running
After setting up the environment variables, you can run the application locally:
```
python3 -m application
```

You should then be able to access the application at http://127.0.0.1:10000 in your browser.
