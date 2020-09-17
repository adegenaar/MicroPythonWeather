import weather as Weather
import animations as animations
import RCWL_0516 as Radar
import time
import config
#from ota_updater import OTAUpdater


def download_and_install_update_if_available():
    # read the credentials from the RTC

    # import machine
    # rtc = machine.RTC()
    # rtc.memory(b'hello')

#    o = OTAUpdater("https://github.com/adegenaar/MicroPythonWeather")
#    o.download_and_install_update_if_available(config.SSID, config.password)
    pass

def boot():
    download_and_install_update_if_available()
    # load the NTP time
    # see if the RTC needs to be updated...


def main():
    # appid = os.environ.get("OPENWEATHERMAP_APPID")
    weather = Weather.weather()
    effects = animations.animations()
    effects.setcolor(animations.black)

    radar = Radar.RCWL_0516()
    radar.begin(15)
    timer = time.time() - float(3600)  # start with the timer off
    while True:
        # if the radar is detecting a person, set the timer for 15 minutes
        if radar.isOn():
            timer = time.time() + float(3600 * 15)  # 15 minutes
        else:
            pass

        # if the timer has expired, sleep and wait for the radar to come on
        if time.time() > timer:
            if effects.np[0] != animations.black:
                effects.setcolor(animations.black)
            time.sleep_ms(50)
            continue

        # retreive the current weather forecast
        weather.getWeather(config.OPENWEATHERMAP_APPID, config.LOCATION)
        ani = None
        if weather.weather == "Thunderstorm":
            ani = effects.lightning
        elif weather.weather in ["Rain", "Drizzle", "Squall","Mist"]:
            ani = effects.flicker

        cloud = animations.white
        if weather.current < 40:
            cloud = animations.blue
        elif weather.current < 70:
            cloud = animations.green
        elif weather.current < 80:
            cloud = animations.gold        
        elif weather.current < 90:
            cloud = (90,0,0)
        else:
            cloud = animations.red

        effects.setcolor(cloud)
        if ani:
            ani()


boot()
main()
