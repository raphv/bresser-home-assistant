# Bresser WiFi Weather Station for Home Assistant

## If you are using the Home Assistant OS, use the add-on in the sibling repository instead [bresser-pws-haos-addon](https://github.com/raphv/bresser-pws-haos-addon)

### If you are *not* using Home Assistant OS, I recommend switching.

The [Bresser WiFi ClearView Weather Station](https://www.bresser.de/en/Weather-Time/BRESSER-WIFI-ClearView-Weather-Station-with-7-in-1-Sensor.html) comprises an external sensor and an indoor base station.
These communicate via a 868 MHz frequency, but the indoor base station also  has WiFi capability.
One benefit of communicating through the indoor station rather than decoding the RF transmission is to access data from sensors that are on the base station itself.
Its capabilities include upload to Weather Underground, but also to any arbitrary Web server, including a local one.
The weather station doesn't expose any open ports so the only way to access data is to create a web server and to listen to requests.

I have created a Python script that listens to requests on `/weatherstation/updateweatherstation.php`, stores this data in a dictionary, then serves it on another URL (`/data`) that Home Assistant can access as sensors via the [REST integration](https://www.home-assistant.io/integrations/rest/).
The Python script also logs weather data as one CSV file per day.

### Installing the Python Script

I recommend using a virtual environment, then install the only dependency in the project, `bottle`

```
USER@raspberrypi:~ $ python3 -m venv weatherlistener/env
USER@raspberrypi:~ $ source weatherlistener/env/bin/activate
(weatherlistener) USER@raspberrypi:~ $ pip install bottle
```

To run it as a service, I have created a file in `/etc/systemd/system` named `weatherlistener@USER.service` where `USER` is replaced by my user name. I can then be called by typing:

```
$ sudo systemctl start weatherlistener@USER
```

### Edit the configuration of your Weather Station

Follow the instruction manual of your weather station and set up the periodic upload of weather data
* Choose other server
* Put homeassistant.local:8000 (or use the IP address of your HA Instance) as the URL

### Check that the data is properly uploaded

* Go to <http://homeassistant.local:8000/data> to see if a JSON file with correct data is present
* You can see whether the weather station has uploaded data by checking the logs of the add on.

An example of proper data update looks like this:

`192.168.1.5 - - [05/Jan/2026 12:00:40] "GET /weatherstation/updateweatherstation.php?ID=id&PASSWORD=key&action=updateraww&realtime=1&rtfreq=5&dateutc=now&baromin=29.90&tempf=31.8&dewptf=30.9&humidity=96&windspeedmph=0.0&windgustmph=0.0&winddir=162&rainin=0.0&dailyrainin=0.0&solarradiation=0.0&UV=0.0&indoortempf=62.4&indoorhumidity=48 HTTP/1.1" 200 2`

## Update your Home Assistant configuration

I am using two methods to expose data to Home Assistant:
* As individual sensor entities using [template sensors](https://www.home-assistant.io/integrations/template/) - this configuration is described in `weatherstation-sensors.yaml`
* As a [Weather Station entity](https://www.home-assistant.io/integrations/weather.template/) - this configuration is described in `weatherstation-template.yaml`
