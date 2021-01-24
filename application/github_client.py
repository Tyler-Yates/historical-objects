import requests
from requests import Response
from requests.auth import HTTPBasicAuth


class GithubClient:
    def __init__(self, username: str, token: str):
        self.username = username
        self.token = token

    def make_request(self, request_url: str) -> Response:
        return requests.get(request_url, auth=HTTPBasicAuth(self.username, self.token))
