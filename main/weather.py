# if wifi is down, flash RED and wait
#
# if someone is around
#
# if we are past the top of the hour,
#   get the weather
#   interpret the weather
# display
#   cycle thru the hours (12/16)
#       bracketed array of temp colors (need Stef's help here)
#       if raining or thunderstorming
#           flicker
#
# import json
import time
import urequests as requests 
import ujson as json

# import os
import pprint


class weather:
    def __init__(self, delay=3600):
        """
        __init__ Constructor

        Args:
            delay (int, optional): Number of seconds between each pull of the weather data. Defaults to 3600.
        """
        self.delay = delay
        self.timer = (
            time.time() - delay
        )  # make sure the first call to getWeather will get the weather
        self.today_high = -1
        self.today_low = -1
        self.current = -1
        self.next_high = -1
        self.next_low = -1
        self.next_forecast = -1
        self.timezone = -14400
        self.sunrise = -1
        self.sunset = -1
        self.weather = ""

    # the main weather indicators are:
    # https://openweathermap.org/weather-conditions
    # Thunderstorm
    # Drizzle
    # Rain
    # Snow
    # Mist
    # Smoke
    # Haze
    # Dust
    # Fog
    # Sand
    # Ash
    # Squall
    # Tornado
    # Clear
    # Clouds

    # Gets weather forecast
    def currentWeather(self, appid, location):
        """
        {
            "coord":{"lon":-84.6,"lat":33.83},
            "weather":[
                {"id":802,"main":"Clouds","description":"scattered clouds","icon":"03n"}
                ],
            "base":"stations",
            "main":{"temp":73.53,"feels_like":79.66,"temp_min":72,"temp_max":75.2,"pressure":1019,"humidity":94},
            "visibility":10000,
            "wind":{"speed":4.21,"deg":72},
            "clouds":{"all":40},
            "dt":1598408493,
            "sys":{"type":1,"id":4155,"country":"US","sunrise":1598353671,"sunset":1598400795},
            "timezone":-14400,
            "id":0,
            "name":"Mableton",
            "cod":200
        }

        """
        # res = requests.request(
        #     "get",
        #     "https://api.openweathermap.org/data/2.5/weather?q={},us&appid={}&units=imperial".format(location,appid)
        # )
        # return res.json()

        res = requests.get("https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}".format(location,appid))
        # ud = res.text
        # raw = ujson.loads(ud)
        # t = raw.get('current').get('temp')
        # w = raw.get('current').get('weather')
        # print(t)
        # print(w)
        return res.json()


    def forecast(self, appid, lat, lon):
        res = requests.request(
            "get",
            "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}&units=imperial&exclude=current".format(lat,lon,appid),
        )
        return res.json()

    def getWeather(self, appid, location):
        # Update weather once every self.delay
        if time.time() - self.timer < self.delay:
            return

        # update the timer
        self.timer = time.time()

        print ('getweather:' + str(time.localtime()))

        # appid = os.environ.get("OPENWEATHERMAP_APPID")
        ##pp = pprint.PrettyPrinter(indent=4)

        weather = self.currentWeather(appid, location)
        #pprint.pprint(weather)

        self.weather = weather["weather"][0]["main"]
        #pprint.pprint(self.weather)
        self.today_high = weather["main"]["temp_max"]
        self.today_low = weather["main"]["temp_min"]
        self.current = weather["main"]["temp"]
        self.timezone = weather["timezone"]
        self.sunrise = weather["sys"]["sunrise"]
        self.sunset = weather["sys"]["sunset"]

        # lat = weather["coord"]["lat"]
        # lon = weather["coord"]["lon"]
        # alltheweather = self.forecast(appid, lat, lon)
        # print("FORECAST")
        # print("---")
        # pp.pprint(alltheweather)
