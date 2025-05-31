from flask import Flask, render_template, request
from weather import get_current_weather, get_forecast_weather 
from datetime import datetime
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    weather_data = None
    forecast_data = None
    error = None
    city = ''
    video_file = 'cloud.mp4'
    three_hourly_data = None

    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            weather_data, state_c = get_current_weather(city)
            forecast_data, state_f, three_hourly_data = get_forecast_weather(city)
            print(weather_data)
            print(forecast_data)

        elif 'lat' in request.form and 'lon' in request.form:
            lat = request.form['lat']
            lon = request.form['lon']
            weather_data, state_c = get_current_weather(lat=lat, lon=lon)
            forecast_data, state_f, three_hourly_data = get_forecast_weather(lat=lat, lon=lon)
            weather_data['city'] = request.form['location']

            if state_c != 200 or state_f != 200:
                error = f"Could not fetch weather data for {city}. Please check the loaction name."
            else:


                # Map weather condition to video file
                weather_main = weather_data['weather_main'].lower() if weather_data else 'default'
                video_map = {
                    'clouds': 'clouds.mp4',
                    'rain': 'rain.mp4',
                    'snow': 'snow.mp4',
                    'thunderstorm': 'rain.mp4',
                    'snow': 'snow.mp4',
                    'clear': 'clear.mp4'
                }
                video_file = video_map.get(weather_main, 'default.mp4')
    
    if three_hourly_data:
        next_12_forecasts = get_next_12_forecasts(three_hourly_data, weather_data)
    else:
        next_12_forecasts = []


    return render_template('index.html', weather=weather_data, forecast=forecast_data, error=error, 
                           city=city, video_file=video_file, next_12_forecasts=next_12_forecasts)

def get_next_12_forecasts(data, current_weather):
    now = datetime.now()
    upcoming_weather = []

    current_forecast = {
        'time': 'Now',
        'date': now.strftime('%Y-%m-%d'),
        'temperature': current_weather['temperature'],
        'weather_main': current_weather['weather_main']
    }
    upcoming_weather.append(current_forecast)

    for entry in data:
        forecast_time = datetime.strptime(f"{entry['date']} {entry['time']}", "%Y-%m-%d %H:%M")
        if forecast_time > now:
            upcoming_weather.append(entry)
        if len(upcoming_weather) == 6:
            break

    return upcoming_weather


if __name__ == '__main__':
    app.run(debug = True)

