import requests
from django.conf import settings

API_KEY = settings.API_KEY

BASE_URL = "http://api.weatherapi.com/v1/"


class Location:
    """
    Location of forecast area
    """

    def __init__(self, city="", postal=""):
        if postal:
            self.q = postal
        else:
            self.q = city

    def _forecastResponse(self):
        return requests.get(
            BASE_URL + "forecast.json",
            params={
                "key": API_KEY,
                "q": self.q,
                "days": 7,
                "alerts": "yes",
                "aqi": "yes",
            },
        )

    def getForecast(self):
        """
        Returns dict of forecast, False if error.
        """
        response = self._forecastResponse()
        if response.status_code == 200:
            return response.json()
        else:
            return False

    def calculateFireRisk(self, temp_c, humidity, wind_kph):
        """
        0: Low fire risk
        1: Moderate fire risk
        2: High fire risk
        3+: Extreme fire risk
        """

        # Define threshold values for each factor (30 30 30 rule)
        tempThreshold = 30  # Celsius
        humidityThreshold = 30  # Percentage
        windThreshold = 30  # km/h

        # Calculate fire risk based on factors' relation to thresholds
        fireRisk = 0

        if temp_c >= tempThreshold:
            fireRisk += 1

        if humidity <= humidityThreshold:
            fireRisk += 1

        if wind_kph >= windThreshold:
            fireRisk += 1

        return fireRisk
