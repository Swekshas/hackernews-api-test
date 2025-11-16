import requests
from core.config import BASE_URL, HEADERS

class APIClient:
    def __init__(self, base_url=BASE_URL, headers=HEADERS):
        self.base_url = base_url
        self.headers = headers

    def get(self, endpoint, params=None):
        return requests.get(f"{self.base_url}{endpoint}", headers=self.headers, params=params)

    def post(self, endpoint, body=None):
        return requests.post(f"{self.base_url}{endpoint}", headers=self.headers, json=body)

    def put(self, endpoint, body=None):
        return requests.put(f"{self.base_url}{endpoint}", headers=self.headers, json=body)

    def delete(self, endpoint):
        return requests.delete(f"{self.base_url}{endpoint}", headers=self.headers)