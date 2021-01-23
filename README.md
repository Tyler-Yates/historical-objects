# historical-objects

## Prerequisites
You will need a [Heroku](https://www.heroku.com/) account and the
[Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) to run this application.
Heroku has a [free tier](https://www.heroku.com/free).
It is recommended that you follow [Heroku's guide](https://devcenter.heroku.com/articles/getting-started-with-python)
to getting started with Python before running this application.

This README assumes you are running on Linux.

You will need a [Python 3](https://www.python.org/about/) interpreter to run this application.
The Python 3 interpreter should include the `venv` module.

## Setup

### Python
You will need to create a virtual environment to run this application.
Run the following commands at the root of this repo:
```
python3 -m venv venv
source venv/bin/activate
pip install -Ur requirements.txt
```

### SSL
To preserve consistency with running in the cloud, this application uses HTTPS even when running locally.
You will need to run the following commands from the root of the repo to get ready for HTTPS:
```
mkdir ssl
cd ssl
openssl req -nodes -new -x509 -keyout server.key -out server.crt \
    -subj "/C=GB/ST=London/L=London/O=Local/OU=Local/CN=127.0.0.1"
```
The `ssl` folder is ignored by `git` so you should not need to worry about committing the
generated key and certificate.

## Running
After setting up the environment variables, you can run the application locally.
Be sure you have activated the virtual environment before running this command:
```
heroku local
```

You should then be able to access the application at [http://0.0.0.0:5000](http://0.0.0.0:5000) in your browser.
