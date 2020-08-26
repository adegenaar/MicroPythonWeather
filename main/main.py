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
    # appid = os.environ.get("OPENWEATHERMAP_APPID")
    OPENWEATHERMAP_APPID = "d7195c6f01d61693cd3a094e2a771437"
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
            time.sleep(3)
            continue

        # retreive the current weather forecast
        weather.getWeather(OPENWEATHERMAP_APPID, "30126")

        ani = None
        if weather.weather == "Thunderstorm":
            ani = effects.lightning
        elif weather.weather in ["Rain", "Drizzle", "Squall"]:
            ani = effects.flicker

        cloud = Colors.white
        if weather.current < 40:
            cloud = Colors.blue
        elif weather.current < 70:
            cloud = Colors.green
        elif weather.current < 80:
            cloud = Colors.gold
        else:
            cloud = Colors.red

        effects.setcolor(cloud)
        if ani:
            ani()


boot()
main()
