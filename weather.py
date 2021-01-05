from datetime import datetime


class Weather:
    def __init__(
        self,
        wx_date=None,
        temp=None,
        feelslike=None,
        pressure=None,
        dewpoint=None,
        humidity=None,
        clouds=None,
        visibility=None,
        wind_speed=None,
        wind_dir=None
    ):

        self.temp = temp
        self.feelslike = feelslike
        self.pressure = pressure
        self.dewpoint = dewpoint
        self.humidity = humidity
        self.clouds = clouds
        self.visibility = visibility
        self.wind_speed = wind_speed
        self.wind_dir = wind_dir
        self.wx_date = wx_date

    @staticmethod
    def from_owm(dict):
        return Weather(
            wx_date=datetime.fromtimestamp(dict.get('dt', '')),
            temp=dict.get('temp', 0),
            feelslike=dict.get('feels_like', 0),
            pressure=dict.get('pressure', 0),
            dewpoint=dict.get('dew_point', 0),
            humidity=dict.get('humidity', 0),
            clouds=dict.get('clouds', 0),
            visibility=dict.get('visibility', 0),
            wind_speed=dict.get('wind_speed', 0),
            wind_dir=dict.get('wind_deg', 0),
        )

    @staticmethod
    def from_weatherstack(dict):
        return Weather(
            wx_date=datetime.fromtimestamp(dict.get('dt', '')),
            temp=dict.get('temperature', 0),
            feelslike=dict.get('feelslike', 0),
            pressure=dict.get('pressure', 0),
            dewpoint=dict.get('dewpoint', 0),
            humidity=dict.get('humidity', 0),
            clouds=dict.get('cloudcover', 0),
            visibility=int(round(dict.get('visibility', 0) * 1609.34)),
            wind_speed=dict.get('wind_speed', 0),
            wind_dir=dict.get('wind_degree', 0),
        )

    def __str__(self):
        output = f"{self.wx_date}"
        output += f"\ntemp: {self.temp}"
        output += f"\nfeels like: {self.feelslike}"
        output += f"\npressure: {self.pressure}"
        output += f"\ndew point: {self.dewpoint}"
        output += f"\nhumidity: {self.humidity}"
        output += f"\nclouds: {self.clouds}"
        output += f"\nvisibility: {self.visibility}"
        output += f"\nwind speed: {self.wind_speed}"
        output += f"\nwind direction: {self.wind_dir}\n"

        return output
