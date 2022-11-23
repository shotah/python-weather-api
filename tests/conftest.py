import json
import re

from pytest import fixture

from src.index import app


@fixture(autouse=True)
def client():
    with app.test_client() as client_:
        yield client_


@fixture(autouse=True)
def weather_api(requests_mock):
    with open("./tests/data/fake_weather_response.json") as file:
        response_data = json.load(file)
    matcher = re.compile("http://api.weatherunlocked.com/api/.*")
    requests_mock.get(matcher, json=response_data)
