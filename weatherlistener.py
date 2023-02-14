from bottle import request, response, route, run
import datetime, json, os

current_data = {}

WIND_DIRS = [
	'N', 'NNE', 'NE', 'ENE',
	'E', 'ESE', 'SE', 'SSE',
	'S', 'SSW', 'SW', 'WSW',
	'W', 'WNW', 'NW', 'NNW'
]

LOGGED_KEYS = [
	'timestamp', 'temperature_c', 'humidity', 'pressure_hpa', 'wind_speed_kmh', 'rain_mm', 'solar_radiation'
]

def deg_to_dir(deg):
	return WIND_DIRS[round(int(deg)/22.5) % 16]

def mph_to_kmh(mph):
	return round(float(mph)*1.609344,1)

def mph_to_ms(mph):
	return round(float(mph)*0.44704,1)

def in_to_mm(inches):
	return round(float(inches)*25.4,1)

def f_to_c(tempf):
	return round((float(tempf)-32)*5/9,1)

def min_to_hpa(pressuremin):
	return round(float(pressuremin)*33.7685)

@route('/weatherstation/updateweatherstation.php')
def receive_data():
	current_data.update({
		"timestamp": datetime.datetime.now().astimezone().replace(microsecond=0).isoformat(),
		"pressure_inhg": float(request.query.baromin),
		"pressure_hpa": min_to_hpa(request.query.baromin),
		"temperature_f": float(request.query.tempf),
		"temperature_c": f_to_c(request.query.tempf),
		"dew_point_f": float(request.query.dewptf),
		"dew_point_c": f_to_c(request.query.dewptf),
		"humidity": int(request.query.humidity),
		"wind_speed_mph": float(request.query.windspeedmph),
		"wind_speed_kmh": mph_to_kmh(request.query.windspeedmph),
		"wind_speed_ms": mph_to_ms(request.query.windspeedmph),
		"wind_gust_mph": float(request.query.windgustmph),
		"wind_gust_kmh": mph_to_kmh(request.query.windgustmph),
		"wind_gust_ms": mph_to_ms(request.query.windgustmph),
		"wind_direction_bearing": int(request.query.winddir),
		"wind_direction_compass": deg_to_dir(request.query.winddir),
		"rain_in": float(request.query.rainin),
		"rain_mm": in_to_mm(request.query.rainin),
		"daily_rain_in": float(request.query.dailyrainin),
		"daily_rain_mm": in_to_mm(request.query.dailyrainin),
		"solar_radiation": float(request.query.solarradiation),
		"uv": float(request.query.UV),
		"temperature_indoor_f": float(request.query.indoortempf),
		"temperature_indoor_c": f_to_c(request.query.indoortempf),
		"humidity_indoor": int(request.query.indoorhumidity),
	})
	logfile = 'logs/weather-%s.csv'%datetime.date.today().isoformat()
	isnewfile = (not os.path.exists(logfile))
	with open(logfile, 'a') as f:
		if isnewfile:
			f.write('%s\n'%(','.join(LOGGED_KEYS)))
		f.write('%s\n'%(','.join(str(current_data[k]) for k in LOGGED_KEYS)))
	return 'OK'

@route('/data')
def show_data():
	response.content_type = 'application/json'
	return json.dumps(current_data)

run(host='0.0.0.0', port='8000')

