from dotenv import load_dotenv, find_dotenv
from requests.exceptions import HTTPError
from datetime import datetime, timedelta
from weather import Weather
import requests
import json
import time
import os


class WeatherStack:

    baseURL = 'https://api.weatherstack.com/historical?'

    def __init__(self, API_KEY):
        self.API_KEY = API_KEY

    def get_date(self):
        return self.weather_date

    def get_location(self):
        return self.lat, self.lon

    def fetch_weather(self, lat, lon, weather_date):

        self.lat = lat
        self.lon = lon
        self.weather_date = weather_date
        # convert datetime to string 'yyyy-mm-dd'
        self.string_date = self.weather_date.strftime('%Y-%m-%d')

        apiURL = f"{self.baseURL}access_key={self.API_KEY}&query={self.lat},{self.lon}&historical_date={self.string_date}&hourly=1&interval=1&units=f"
        # print(apiURL)

        try:
            response = requests.get(apiURL)

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        # else:
        #     print('Success!')

        self.response_status = response.status_code
        self.weather_json = response.json()

        self.weather_json = self.weather_json.get('historical', {}).get(
            self.string_date, {}).get('hourly', [])[self.weather_date.hour]

        request_timestamp = response.json().get(
            'location', {}).get('localtime_epoch', None)

        utc_timestamp = int(
            round(
                datetime.utcfromtimestamp(request_timestamp).timestamp()
            )
        )
        request_timestamp = utc_timestamp

        self.weather_json.setdefault('dt', utc_timestamp)

        self.weather_data = Weather.from_weatherstack(self.weather_json)
        # output = json.dumps(self.weather_json, sort_keys=True, indent=4)
        # print(output)

        return self.response_status

    def print_weather(self):

        if(self.response_status != 200):
            print(f"Status Code: {self.response_status}")
        else:
            print(self.weather_date)
            print(self.weather_data)


if(__name__ == "__main__"):
    load_dotenv(find_dotenv())
    API_KEY = os.getenv("WEATHERSTACK_API")
    wswx = WeatherStack(API_KEY)

    wxdate = datetime.now() - timedelta(minutes=1)
    lat = os.getenv("LATITUDE")
    lon = os.getenv("LONGITUDE")

    wswx.fetch_weather(lat, lon, wxdate)

    myweather = wswx.weather_data
    print(myweather)
    print(f"\n{myweather.wx_date} temp: {myweather.temp}° (feels like: {myweather.feelslike}°)")
