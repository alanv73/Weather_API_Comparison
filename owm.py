from dotenv import load_dotenv, find_dotenv
from requests.exceptions import HTTPError
from datetime import datetime, timedelta
from weather import Weather
import requests
import json
import time
import os


class OWM_OneCall:

    baseURL = 'http://api.openweathermap.org/data/2.5/onecall/timemachine?'

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
        # convert datetime to unix timestamp
        self.unixtime = int(
            round(
                time.mktime(self.weather_date.timetuple())
            )
        )

        apiURL = f"{self.baseURL}lat={self.lat}&lon={self.lon}&dt={self.unixtime}&appid={self.API_KEY}&units=imperial"
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
        self.weather_json = response.json().get('current', '{}')
        self.weather_data = Weather.from_owm(self.weather_json)

        return self.response_status

    def print_weather(self):

        if(self.response_status != 200):
            print(f"Status Code: {self.response_status}")
        else:
            print(self.weather_date)
            print(self.weather_data)


if(__name__ == "__main__"):
    load_dotenv(find_dotenv())
    API_KEY = os.getenv("OWM_API")
    ocwx = OWM_OneCall(API_KEY)

    wxdate = datetime.now() - timedelta(minutes=1)
    lat = os.getenv("LATITUDE")
    lon = os.getenv("LONGITUDE")

    ocwx.fetch_weather(lat, lon, wxdate)

    myweather = ocwx.weather_data
    print(myweather)
    print(f"\n{myweather.wx_date} temp: {myweather.temp}° (feels like: {myweather.feelslike}°)")
