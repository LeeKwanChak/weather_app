from flask import Flask, render_template, request
from weather import get_current_weather, get_forecast_weather, get_upcoming_forecast
app = Flask(__name__)


# Flask routes
@app.route('/', methods = ['GET', 'POST'])
def index():
    # variable definitions and initialization for sending data to frontend later
    weather_data = None
    forecast_data = None
    error = None
    location = ''
    three_hourly_data = None

    # Process request from user
    if request.method == 'POST':
        location = request.form.get('location_input')
        if location: # if user search a location
            weather_data, state_c = get_current_weather(location)

            if(state_c != 200): # != 200 means incorrect location name
                weather_data = None
                forecast_data = None
                three_hourly_data = None
                error = f"Could not search weather data for {location}. Please check the loaction name."
            else:
                forecast_data, state_f, three_hourly_data = get_forecast_weather(location) # else correct location name, program storing the data


        # else if user use the location dection button
        elif 'lat' in request.form and 'lon' in request.form: 
            lat = request.form['lat']
            lon = request.form['lon']
            weather_data, state_c = get_current_weather(lat=lat, lon=lon) # search location using latitude and longitude
            forecast_data, state_f, three_hourly_data = get_forecast_weather(lat=lat, lon=lon)
            weather_data['location'] = request.form['location']

    
    if three_hourly_data:
        upcoming_weather = get_upcoming_forecast(three_hourly_data, weather_data) # get data for frontend chart
    else:
        upcoming_weather = []

    return render_template('index.html', weather = weather_data, forecast = forecast_data, error = error, 
                           location = location, next_12_forecasts = upcoming_weather)


if __name__ == '__main__':
    app.run(debug = False)

