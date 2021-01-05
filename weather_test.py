from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timedelta
from weatherstack import WeatherStack
from numbar import printNumBar
from owm import OWM_OneCall
from dateutil import rrule
import random
import os

load_dotenv(find_dotenv())
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API")
OWM_API_KEY = os.getenv("OWM_API")
lat = os.getenv("LATITUDE")
lon = os.getenv("LONGITUDE")

now_timestamp = datetime.now()
five_days_ago = now_timestamp - timedelta(days=5)

days = [
    dt.date() for dt in rrule.rrule(
        rrule.DAILY,
        dtstart=five_days_ago.date(),
        until=now_timestamp.date()
    )
]

data = []
wswx = WeatherStack(WEATHERSTACK_API_KEY)
owmwx = OWM_OneCall(OWM_API_KEY)

date_count = 0
total_dates = 0

for day in days:

    hours = [hour for hour in range(24)]
    total_dates = len(days) * len(hours)

    for hr in hours:

        top_hour = datetime(day.year, day.month, day.day, hr)
        print(
            printNumBar(
                date_count,
                total_dates,
                decimals=0,
                length=60,
                bar_label=f"{int(round((date_count/total_dates) * 100))}%",
                print_output=False
            ),
            end='\r'
        )
        date_count += 1

        if (top_hour >= five_days_ago) and ((top_hour + timedelta(hours=1)) < datetime.now()):
            while True:
                next_datetime = datetime(
                    day.year, day.month, day.day, hr, random.randint(0, 59))
                if next_datetime >= five_days_ago:

                    # print(next_datetime.strftime(
                    #     '%m/%d/%y %I:%M %p'), end='\r')
                    next_element = {}
                    next_element['date'] = next_datetime

                    wswx.fetch_weather(lat, lon, next_datetime)
                    next_element['weatherstack'] = wswx.weather_data

                    owmwx.fetch_weather(lat, lon, next_datetime)
                    next_element['owm'] = owmwx.weather_data

                    data.append(next_element)

                    break

print()
filename = 'wx_data.csv'
file = open(filename, "w")
file.write(
    "date,owm temp,ws temp,owm feelslike,ws feelslike,owm pressure,ws pressure,owm dewpoint,ws dewpoint,owm humidity,ws humidity,owm clouds,ws clouds,owm visibility,ws visibility,owm wind_speed,ws wind_speed,owm wind_dir,ws wind_dir\n")

for datum in data:
    print(datum.get('date', None))
    print(f"\ttemp:\t{datum['owm'].temp}\t{datum['weatherstack'].temp}")
    print(
        f"\tfeels like:\t{datum['owm'].feelslike}\t{datum['weatherstack'].feelslike}")
    print(
        f"\tpressure:\t{datum['owm'].pressure}\t{datum['weatherstack'].pressure}")
    print(
        f"\tdewpoint:\t{datum['owm'].dewpoint}\t{datum['weatherstack'].dewpoint}")
    print(
        f"\thumidity:\t{datum['owm'].humidity}\t{datum['weatherstack'].humidity}")
    print(
        f"\tclouds:\t{datum['owm'].clouds}\t{datum['weatherstack'].clouds}")
    print(
        f"\tvisibility:\t{datum['owm'].visibility}\t{datum['weatherstack'].visibility}")
    print(
        f"\twind_speed:\t{datum['owm'].wind_speed}\t{datum['weatherstack'].wind_speed}")
    print(
        f"\twind_dir:\t{datum['owm'].wind_dir}\t{datum['weatherstack'].wind_dir}")

    file.write(f"{datum.get('date', None)},{datum['owm'].temp},{datum['weatherstack'].temp},{datum['owm'].feelslike},{datum['weatherstack'].feelslike},{datum['owm'].pressure},{datum['weatherstack'].pressure},{datum['owm'].dewpoint},{datum['weatherstack'].dewpoint},{datum['owm'].humidity},{datum['weatherstack'].humidity},{datum['owm'].clouds},{datum['weatherstack'].clouds},{datum['owm'].visibility},{datum['weatherstack'].visibility},{datum['owm'].wind_speed},{datum['weatherstack'].wind_speed},{datum['owm'].wind_dir},{datum['weatherstack'].wind_dir}\n")

file.close()
