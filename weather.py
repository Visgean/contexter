from datetime import datetime, timedelta
from collections import namedtuple, defaultdict

import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"


class ForecastPerDay:
    def __init__(self):
        self.vmin = float("inf")
        self.vmax = float("-inf")
        self.hours_with_rain = []

    def __str__(self):
        if self.hours_with_rain:
            rain_h = ", ".join(map(str, self.hours_with_rain))
            rain = f"it will rain on hours: {rain_h}."
        else:
            rain = "no rain forecasted."
        return f"Max temp: {self.vmax:0.1f}C, min temp: {self.vmin:0.1f}C, {rain}"


def get_weather_forecast(lat=50.088, lng=14.4208):
    params = {
        "latitude": lat,
        "longitude": lng,
        "hourly": ["temperature_2m", "rain"],
        "models": "ecmwf_ifs025",
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_rain = hourly.Variables(1).ValuesAsNumpy()

    fcast = defaultdict(lambda: ForecastPerDay())

    current_hour = datetime.fromtimestamp(hourly.Time())
    for temp, rain in zip(hourly_temperature_2m, hourly_rain):
        dt = current_hour.date()
        if fcast[dt].vmin > temp:
            fcast[dt].vmin = temp
        if fcast[dt].vmax < temp:
            fcast[dt].vmax = temp

        if rain > 0.3:
            fcast[dt].hours_with_rain.append(current_hour.hour)

        current_hour += timedelta(hours=1)

    return "".join([f"{day}: {fcast}" for day, fcast in fcast.items()])
