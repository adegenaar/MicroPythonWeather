import weather
import animations
import rcwl_0516
import time

from ota_update.main.ota_updater import OTAUpdater


def download_and_install_update_if_available():
    # read the credentials from the RTC

    # import machine
    # rtc = machine.RTC()
    # rtc.memory(b'hello')

    o = OTAUpdater("https://github.com/adegenaar/${REPO_NAME}")
    o.download_and_install_update_if_available("fred", "yellow:sticky")


def boot():
    download_and_install_update_if_available()
    # load the NTP time
    # see if the RTC needs to be updated...


def main():
    weather = weather.weather()
    effects = animations.animations()
    radar = rcwl_0516()
    radar.begin()
    timer = time.time() - 3600  # start with the timer off

    while True:
        # if the radar is detecting a person, set the timer for 15 minutes
        if radar.isOn():
            timer = time.time() + 3600 * 15  # 15 minutes

        # if the timer has expired, sleep and wait for the radar to come on
        if time.time() < timer:
            time.sleep(1)
            continue

        # retreive the current weather forecast
        weather.getWeather()

        # Check forecast codes to make sure none are rain or snow https://developer.yahoo.com/weather/documentation.html
        flicker = 1
        if weather in [
            "24",
            "26",
            "27",
            "28",
            "29",
            "30",
            "31",
            "32",
            "33",
            "34",
            "36",
            "44",
        ]:
            flicker = 0

        # blue is the default color, followed by gold, followed by red
        cloud = Colors.blue

        # Subtracts 10% from todays low than checks to see if that is greater than tomorrows low.
        # If tomorrow is more than 10% colder the cloud should be gold
        if (int(weather.today_low) - (int(weather.today_low) * 0.1)) > int(
            weather.next_low
        ):
            cloud = Colors.gold

        # Adds 10% to todays high than checks to see if that is less than tomorrows high.
        # If tomorrow is more than 10% hotter cloud should be red
        if ((int(weather.today_high) * 0.1) + int(weather.today_high)) < int(
            weather.next_high
        ):
            cloud = Colors.red

        if flicker == 0:
            effects.setcolor(cloud)  # Solid Red Cloud
        else:
            effects.flicker(cloud)


boot()
main()
