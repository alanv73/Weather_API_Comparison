from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timedelta
from weatherstack import WeatherStack
import matplotlib.pyplot as plt
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


def get_data():
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

                        next_element = {}
                        next_element['date'] = next_datetime

                        wswx.fetch_weather(lat, lon, next_datetime)
                        next_element['weatherstack'] = wswx.weather_data

                        owmwx.fetch_weather(lat, lon, next_datetime)
                        next_element['owm'] = owmwx.weather_data

                        data.append(next_element)

                        break
    return data


def get_chart_data(parameter, data):
    x_axis = []
    ws_parameter = []
    owm_parameter = []

    for datum in data:
        x_axis.append(datum.get('date', ''))

        ws_data = datum.get('weatherstack', 0)
        ws_parameter.append(ws_data.__getattribute__(parameter))

        owm_data = datum.get('owm', 0)
        owm_parameter.append(owm_data.__getattribute__(parameter))

    chart_data = {}
    chart_data['x-axis'] = x_axis
    chart_data['ws-parameter'] = ws_parameter
    chart_data['owm-parameter'] = owm_parameter

    return chart_data


def show_chart(parameter, data):
    chart_data = get_chart_data(parameter, data)

    x_axis = chart_data['x-axis']
    ws_parameter = chart_data['ws-parameter']
    owm_parameter = chart_data['owm-parameter']

    # print(x_axis)
    # print(ws_parameter)
    # print(owm_parameter)

    fig, ax = plt.subplots()
    # ax1, ax2 = [ax, ax.twinx()]
    fig.canvas.set_window_title(f"{parameter.title()}")
    fig.autofmt_xdate()
    ax.plot(
        x_axis,
        ws_parameter,
        label='Weatherstack',
        color='Blue',
        linewidth=3.0
    )
    ax.plot(
        x_axis,
        owm_parameter,
        label='Open Weather Map',
        color='Orange',
        linewidth=3.0
    )

    plt.title(
        f"API Data Comparison - {parameter.title()}"
    )
    ax.legend(loc='best')
    ax.grid(True, linestyle=':', which='major', axis='y')

    plt.show()


def print_data(data):
    print()

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


def save_data(data):
    filename = 'wx_data.csv'
    file = open(filename, "w")
    file.write(
        "date,owm temp,ws temp,owm feelslike,ws feelslike,owm pressure,ws pressure,owm dewpoint,ws dewpoint,owm humidity,ws humidity,owm clouds,ws clouds,owm visibility,ws visibility,owm wind_speed,ws wind_speed,owm wind_dir,ws wind_dir\n")

    for datum in data:
        file.write(f"{datum.get('date', None)},{datum['owm'].temp},{datum['weatherstack'].temp},{datum['owm'].feelslike},{datum['weatherstack'].feelslike},{datum['owm'].pressure},{datum['weatherstack'].pressure},{datum['owm'].dewpoint},{datum['weatherstack'].dewpoint},{datum['owm'].humidity},{datum['weatherstack'].humidity},{datum['owm'].clouds},{datum['weatherstack'].clouds},{datum['owm'].visibility},{datum['weatherstack'].visibility},{datum['owm'].wind_speed},{datum['weatherstack'].wind_speed},{datum['owm'].wind_dir},{datum['weatherstack'].wind_dir}\n")

    file.close()
    print(f"data saved to {filename}")


def display_title_bar():

    if os.name == 'nt':  # for windows
        os.system('cls')
    else:  # for mac and linux(here, os.name is 'posix')
        os.system('clear')

    print("\t********************************")
    print("\t******  Weather API Test  ******")
    print("\t********************************")


def show_menu():
    active_menu = 'main'

    print("\n\t[1] Get Data from APIs")
    print("\t[2] Print Weather Data")
    print("\t[3] Save Weather Data")
    print("\t[t] Display Temp Chart")
    print("\t[p] Display Pressure Chart")
    print("\t[d] Display Dew Point Chart")
    print("\t[h] Display Humidity Chart")
    print("\t[c] Display Cloud Chart")
    print("\t[v] Display Visibility Chart")
    print("\t[ws] Display Wind Speed Chart")
    print("\t[wd] Display Wind Direction Chart")
    print("\t[q] Quit")

    return input("\n\tSelection? ")


wx_data = None
command = ''
display_title_bar()

while command != 'q':
    command = show_menu()

    display_title_bar()
    if command == '1':
        wx_data = get_data()

        print()
        input("PRESS ENTER TO CONTINUE")
        display_title_bar()

    elif command == '2':
        if wx_data != None:
            print_data(wx_data)
            print()
            input("PRESS ENTER TO CONTINUE")
            display_title_bar()

    elif command == '3':
        if wx_data != None:
            save_data(wx_data)
            print()
            input("PRESS ENTER TO CONTINUE")
            display_title_bar()

    elif command == 't':
        if wx_data != None:
            show_chart('temp', wx_data)
            display_title_bar()

    elif command == 'f':
        if wx_data != None:
            show_chart('feelslike', wx_data)
            display_title_bar()

    elif command == 'p':
        if wx_data != None:
            show_chart('pressure', wx_data)
            display_title_bar()

    elif command == 'd':
        if wx_data != None:
            show_chart('dewpoint', wx_data)
            display_title_bar()

    elif command == 'h':
        if wx_data != None:
            show_chart('humidity', wx_data)
            display_title_bar()

    elif command == 'c':
        if wx_data != None:
            show_chart('clouds', wx_data)
            display_title_bar()

    elif command == 'v':
        if wx_data != None:
            show_chart('visibility', wx_data)
            display_title_bar()

    elif command == 'ws':
        if wx_data != None:
            show_chart('wind_speed', wx_data)
            display_title_bar()

    elif command == 'wd':
        if wx_data != None:
            show_chart('wind_dir', wx_data)
            display_title_bar()
