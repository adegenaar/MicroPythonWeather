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
#           flash white
#
import json
import time


class weather:
    def __init__(self, delay=3600):
        """
        __init__ Constructor

        Args:
            delay (int, optional): Number of seconds between each pull of the weather data. Defaults to 3600.
        """
        self.delay = delay
        self.timer = (
            time.time() - delay()
        )  # make sure the first call to getWeather will get the weather
        self.today_high = -1
        self.today_low = -1
        self.next_high = -1
        self.next_low = -1
        self.next_forecast = -1

    # Gets weather forecast
    def getWeather(self):
        # Update weather once every self.delay
        if time.time() - self.timer < self.delay:
            return False

        # update the timer
        timer = time.time()

        # TODO: update to use a different weather service

        # Change to your location
        url = requests.get(
            'https://query.yahooapis.com/v1/public/yql?q=select item.forecast from weather.forecast where woeid in (select woeid from geo.places(1) where text="sheboygan, wi")&format=json'
        )
        global weather
        weather = json.loads(url.text)

        # Gets todays High and Low
        self.today_high = weather["query"]["results"]["channel"][0]["item"]["forecast"][
            "high"
        ]
        self.today_low = weather["query"]["results"]["channel"][0]["item"]["forecast"][
            "low"
        ]

        # Gets tomorrows High and Low
        self.next_high = weather["query"]["results"]["channel"][1]["item"]["forecast"][
            "high"
        ]
        self.next_low = weather["query"]["results"]["channel"][1]["item"]["forecast"][
            "low"
        ]

        # Get weather code of tomorrows forecast
        self.next_forecast = weather["query"]["results"]["channel"][1]["item"][
            "forecast"
        ]["code"]

        print("updated weather")
        print("todays high is", int(self.today_high))
        print("todays low is", int(self.today_low))
        print("tomorrows code is", int(self.next_forecast))
        print("next high is", int(self.next_high))
        print("next low is", int(self.next_low))
        return True
