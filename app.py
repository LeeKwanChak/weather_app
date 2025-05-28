from flask import Flask, render_template, request
from weather import get_current_weather, get_forecast_weather 
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    weather_data = None
    forecast_data = None
    error = None
    city = ''
    video_file = 'cloud.mp4'

    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            weather_data, state_c = get_current_weather(city)
            forecast_data, state_f = get_forecast_weather(city)
            print(weather_data)
            print(forecast_data)

        elif 'lat' in request.form and 'lon' in request.form:
            lat = request.form['lat']
            lon = request.form['lon']
            weather_data, state_c = get_current_weather(lat=lat, lon=lon)
            forecast_data, state_f = get_forecast_weather(lat=lat, lon=lon)
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

    return render_template('index.html', weather=weather_data, forecast=forecast_data, error=error, city=city, video_file=video_file)

if __name__ == '__main__':
    app.run(debug = True)