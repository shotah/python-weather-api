import json
import os
from typing import Optional

import requests
from aws_lambda_powertools import Logger

logger = Logger()


class Weather:
    WEATHER_API_URL = os.getenv("WEATHER_API_URL")
    WEATHER_API_APP = os.getenv("WEATHER_API_APP")
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    WEATHER_PARAMS = {"app_id": WEATHER_API_APP, "app_key": WEATHER_API_KEY}

    def __init__(self) -> None:
        """
        Vars will be coming from AWS Environmental Vars when in AWS,
        Using this as a stop gap so we don't have to maintain .env AND env.json files.
        """
        settings_file = "./env.json"
        if (
            not self.WEATHER_API_URL
            and not self.WEATHER_API_APP
            and not self.WEATHER_API_KEY
        ):
            if not os.path.exists(settings_file):
                raise ValueError(
                    f"Not able to find connection params in {settings_file}"
                )
            with open(settings_file) as file:
                data = json.load(file)
            self.WEATHER_API_URL = data["Function"]["WEATHER_API_URL"]
            self.WEATHER_API_APP = data["Function"]["WEATHER_API_APP"]
            self.WEATHER_API_KEY = data["Function"]["WEATHER_API_KEY"]
            self.WEATHER_PARAMS = {
                "app_id": self.WEATHER_API_APP,
                "app_key": self.WEATHER_API_KEY,
            }

    def __weather_quote(
        self, high: Optional[int] = None, low: Optional[int] = None
    ) -> str:
        """
        Announcements based on high and low of the days.
        """
        if high and high > 60:
            return "Wow, it's hot." if high > 80 else "What a nice day."
        if low and low < 50:
            return "Brr, it's cold." if low < 30 else "Better get a jacket."
        return "It's just a regular day."

    def __format_day(self, day: dict) -> dict:
        """
        Formats the day body according to our requirements
        """
        return {
            day["date"]: {
                "high": day["temp_max_f"],
                "low": day["temp_min_f"],
                "weather": day["Timeframes"][0]["wx_desc"],
                "announcement": self.__weather_quote(
                    high=day["temp_max_f"], low=day["temp_min_f"]
                ),
            }
        }

    def __format_weather(self, *, data: dict, days: Optional[int]) -> list[dict]:
        """
        Day logic and map and list logic to simplify weather
        """
        data_days = data.get("Days", [])[0:days] if days else data.get("Days", [])
        return list(map(self.__format_day, data_days))

    def get_weather(
        self, *, latitude: float, longitude: float, days: Optional[int]
    ) -> dict:
        """
        Method:
        Main method to call weather api to get back the raw weather data

        Notes:
        lat, lon, and days come in here to increase performance and
        flexibility of the class.
        """
        logger.info(
            {
                "get_weather": {
                    "latitude": latitude,
                    "longitude": longitude,
                    "days": days,
                }
            }
        )
        try:
            url = f"{self.WEATHER_API_URL}/forecast/{latitude},{longitude}?"
            weather_response = requests.request(
                method="GET", url=url, params=self.WEATHER_PARAMS
            )
            logger.info({"get_weather": {"status_code": weather_response.status_code}})
            if not str(weather_response.status_code).startswith("20"):
                return {
                    "message": f"Unable to connect to {self.WEATHER_API_URL}",
                    "status_code": weather_response.status_code,
                }
            return {
                f"{latitude}, {longitude}": self.__format_weather(
                    data=weather_response.json(), days=days
                )
            }
        except Exception as Error:
            return {
                "message": f"Internal Service Error: {Error}",
                "status_code": 500,
            }
