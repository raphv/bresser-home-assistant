# Bresser WiFi Weather Station for Home Assistant

The [Bresser WiFi ClearView Weather Station](https://www.bresser.de/en/Weather-Time/BRESSER-WIFI-ClearView-Weather-Station-with-7-in-1-Sensor.html) comprises an external sensor and an indoor base station.
These communicate via a 868 MHz frequency, but the indoor base station also  has WiFi capability.
One benefit of communicating through the indoor station rather than decoding the RF transmission is to access data from sensors that are on the base station itself.
Its capabilities include upload to Weather Underground, but also to any arbitrary Web server, including a local one.
The weather station doesn't expose any open ports so the only way to access data is to create a web server and to listen to requests.

I have created a Python script that listens to requests on `/weatherstation/updateweatherstation.php`, stores this data in a dictionary, then serves it on another URL (`/data`) that Home Assistant can access as sensors via the [REST integration](https://www.home-assistant.io/integrations/rest/).
The Python script also logs weather data as one CSV file per day.

I recommend using a virtual environment, then install the only dependency in the project, `bottle`

```
USER@raspberrypi:~ $ python3 -m venv weatherlistener/env
USER@raspberrypi:~ $ source weatherlistener/env/bin/activate
(weatherlistener) USER@raspberrypi:~ $ pip inst
```

To run it as a service, I have created a file in `/etc/systemd/system` named `weatherlistener@USER.service` where `USER` is replaced by my user name. I can then be called by typing:

```
$ sudo systemctl start weatherlistener@USER
```

I am using two methods to expose data to Home Assistant:
* As individual sensor entities using [template sensors](https://www.home-assistant.io/integrations/template/) - this configuration is described in `weatherstation-sensors.yaml`
* As a [Weather Station entity](https://www.home-assistant.io/integrations/weather.template/) - this configuration is described in `weatherstation-template.yaml`
