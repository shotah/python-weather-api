import json
import re
from urllib import parse

from aws_lambda_powertools import Logger

logger = Logger()


def test_default_route(client):
    """
    Tests root path to validate it is just returning the path that was it used.
    """
    path = "/"
    resp = client.get(path)
    logger.info(resp.json)
    assert resp.json["path"] == path


def test_weather_route(client):
    """
    Tests weather route with fake data set and checks for correct response
    """
    params = {"latitude": "47.58", "longitude": "-122.30", "days": "3"}
    path = "/weather?" + parse.urlencode(params)
    logger.info({"path": path})
    resp = client.get(path)
    json_data = resp.json
    logger.info(json.dumps(json_data, indent=4, sort_keys=True))
    assert (
        json_data["47.58, -122.3"][0]["23/11/2024"]["announcement"] == "Brr, it's cold."
    )


def test_weather_route_empty_json_response(client, requests_mock):
    """
    Tests weather route with fake data set and checks for correct response
    """
    matcher = re.compile("http://api.weatherunlocked.com/api/.*")
    requests_mock.get(matcher, json={})
    params = {"latitude": "47.58", "longitude": "-122.30", "days": "3"}
    path = "/weather?" + parse.urlencode(params)
    logger.info({"path": path})
    resp = client.get(path)
    json_data = resp.json
    logger.info(json.dumps(json_data, indent=4, sort_keys=True))
    assert json_data["47.58, -122.3"] == []


def test_weather_route_no_json_response(client, requests_mock):
    """
    Tests weather route with fake data set and checks for correct response
    """
    matcher = re.compile("http://api.weatherunlocked.com/api/.*")
    requests_mock.get(matcher)
    params = {"latitude": "47.58", "longitude": "-122.30", "days": "3"}
    path = "/weather?" + parse.urlencode(params)
    logger.info({"path": path})
    resp = client.get(path)
    json_data = resp.json
    logger.info(json.dumps(json_data, indent=4, sort_keys=True))
    assert json_data["47.58, -122.3"][0]["status_code"] == 500
    assert (
        json_data["47.58, -122.3"][0]["error"]
        == "Expecting value: line 1 column 1 (char 0)"
    )


def test_weather_route_remote_api_returns_not_200(client, requests_mock):
    """
    Tests weather route with fake data set and checks for correct response
    """
    matcher = re.compile("http://api.weatherunlocked.com/api/.*")
    requests_mock.get(matcher, status_code=400)
    params = {"latitude": "47.58", "longitude": "-122.30", "days": "3"}
    path = "/weather?" + parse.urlencode(params)
    logger.info({"path": path})
    resp = client.get(path)
    json_data = resp.json
    logger.info(json.dumps(json_data, indent=4, sort_keys=True))
    assert json_data["47.58, -122.3"][0]["status_code"] == 400
