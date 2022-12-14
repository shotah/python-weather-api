from apig_wsgi import make_lambda_handler
from aws_lambda_powertools import Logger
from flask import Flask, jsonify, request
from markupsafe import escape

from .weather import Weather

logger = Logger()
app = Flask(__name__)
app.url_map.strict_slashes = False

handler = make_lambda_handler(app)
# initialize class here to keep it loaded in the lambda to reduce spin up times
weather = Weather()


@app.route("/", methods=["GET"])
def default_endpoint():
    """ "
    Test and health endpoint
    """
    response = {"path": request.path}
    logger.info({"default_endpoint": response})
    return jsonify(response)


@app.route("/weather", methods=["GET"])
def weather_endpoint():
    """
    EXAMPLE:
        curl 'http://127.0.0.1:3000/weather?latitude=47.58&longitude=-122.30&days=3'
    PARAMS: {
        latitude: "47.58",
        longitude: "122.30",
        days: "1"
    }
    RESPONSE:
    {
        "47.58, 122.30": [
            {
                "23/11/2022": {
                    "announcement": "Brr, it's cold.",
                    "high": 28.0,
                    "low": 9.6,
                    "weather": "Sunny skies"
                }
            }
        ]
    }
    """
    # import and clean args
    try:
        latitude = float(escape(request.args.get("latitude")))
        longitude = float(escape(request.args.get("longitude")))
        days = int(escape(request.args.get("days")))
    except Exception:
        return "Error: validating one of the following [Latitude, Longitude, Days]", 400

    # call weather and return response
    try:
        response = weather.get_weather(
            latitude=latitude, longitude=longitude, days=days
        )
        logger.info({"weather_endpoint response": response})
        return jsonify(response)
    except Exception as error:
        return f"Error: {error}", 500
