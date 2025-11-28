from typing import TypeVar
import requests

JSON = TypeVar('JSON')

class FastAPI:
    def __init__(self, url, method = 'POST'):
        self.method = method
        self.url = url

    def __call__(self, example) -> list[JSON]:
        data = example['inputs']["kwargs"]
        match self.method.upper():
            case 'GET':
                response = requests.get(self.url, params = data)
            case 'POST':
                response = requests.post(self.url, json = data)
        return [response.json()]
