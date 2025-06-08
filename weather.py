import requests
from dotenv import load_dotenv
import os
from datetime import datetime
API_KEY = os.getenv('API_KEY')

def get_current_weather(location= None, lat = None, lon = None):

    if location: # if user seach location in a input bar
        url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric'
    elif lat and lon: # if user use the location detection button 
        url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'


    try:
        res = requests.get(url) # request the data from OpenWeatherMap
        current_data = res.json()

        state = current_data['cod'] # check if recieve a vaild data
        if state != 200: # if it is not a correct location name
            return None, state
        
        timezone_offset_seconds = current_data['timezone']
        last_update = datetime.utcfromtimestamp(current_data['dt'] + timezone_offset_seconds).strftime('%H:%M')

        # storing the current data
        current_weather = {
            'location' : current_data['name'],
            'temperature' : round(current_data['main']['temp'],1),
            'weather_main' : current_data['weather'][0]['main'],
            'description': current_data['weather'][0]['description'].capitalize(),
            'humidity': current_data['main']['humidity'],
            'wind_speed': round(current_data['wind']['speed']*3.6),
            'timezone': current_data['timezone'],
            'dt': current_data['dt'],
            'last_update': last_update,
            'local_date_formatted': datetime.utcfromtimestamp(current_data['dt'] + current_data['timezone']).strftime('%a, %b %d'),
            'is_daytime': current_data['dt'] >= current_data['sys']['sunrise'] and current_data['dt'] < current_data['sys']['sunset'],
            'sunrise' : current_data['sys']['sunrise'],
            'sunset': current_data['sys']['sunset']
        }
        return current_weather,state # return data to app.py
    
    except requests.RequestException as e:
        print(f"Error fetching current weather: {e}")
        return None, 'error'


# forecast data for chart and next five day card
def get_forecast_weather(location = None, lat = None, lon = None):
    if location:
        forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={API_KEY}&units=metric'
    elif lat and lon:
        forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'


    try:
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()
        state = int(forecast_data['cod'])

        print('before' , str(forecast_data))

        if state != 200:
            print(f"API Error (forecast): {forecast_data.get('message', 'Unknown error')}")
            return None, state

        forecast_list = []
        daily_data = {}
        three_hourly_data = []

        for data in forecast_data['list']:
            #Group data by date in daily_data
            entry_datetime = datetime.strptime(data['dt_txt'], '%Y-%m-%d %H:%M:%S')
            entry_date = entry_datetime.date()
            entry_time = entry_datetime.time()
            
            # stroging data by date
            date_str = entry_date.strftime('%Y-%m-%d')
            if date_str not in daily_data:
                daily_data[date_str] = {'temps': [], 'weather_inform': []}
            daily_data[date_str]['temps'].append(data['main']['temp'])
            daily_data[date_str]['weather_inform'].append({'time': entry_time, 'weather_main': data['weather'][0]['main']})
            

            # Add three hourly forecast data into three_hourly_data
            dt_txt = data['dt_txt']  # e.g., "2025-05-27 15:00:00"
            entry_datetime = datetime.strptime(dt_txt, '%Y-%m-%d %H:%M:%S')

            # Data for frontend chart
            three_hourly_data.append({
                'time': entry_datetime.strftime('%H:%M'),
                'date': entry_datetime.strftime('%Y-%m-%d'),
                'temperature': round(data['main']['temp'], 1),
                'weather_main': data['weather'][0]['main'],
            })

        # Get next five day forecast data
        for date_str in sorted(daily_data.keys()):
            temps = daily_data[date_str]['temps']
            weather_inform = daily_data[date_str]['weather_inform']
            min_temp = round(min(temps))
            max_temp = round(max(temps))
            weather_main = weather_inform[0]['weather_main']

            for info in weather_inform:
                if 9 <= info['time'].hour <= 15:
                    weather_main = info['weather_main']
                    break
            entry_date = datetime.strptime(date_str, '%Y-%m-%d')
            forecast_list.append({
                'date_formatted': entry_date.strftime('%a, %b %d'),
                'min_temp': min_temp,
                'max_temp': max_temp,
                'weather_main': weather_main
            })


        return forecast_list, state, three_hourly_data # return data to app.py
    except requests.RequestException as e:
        print(f"Error fetching forecast weather: {e}")
        return None, 'error', None


def get_upcoming_forecast(data, current_weather):
    local_now = datetime.utcfromtimestamp(current_weather['dt'] + current_weather['timezone'])
    upcoming_weather = []

    sunrise = datetime.utcfromtimestamp(current_weather['sunrise'] + current_weather['timezone'])
    sunset = datetime.utcfromtimestamp(current_weather['sunset'] + current_weather['timezone'])

    # add now to the list, let user know what is the current weather in the chart
    current_forecast = { 
        'time': 'Now',
        'date': local_now.strftime('%Y-%m-%d'),
        'temperature': current_weather['temperature'],
        'weather_main': current_weather['weather_main'],
        'forecast_isDaytime': sunrise <= local_now <= sunset
    }
    upcoming_weather.append(current_forecast)
    # add upcoming weather to the list
    for entry in data:
        forecast_time = datetime.strptime(f"{entry['date']} {entry['time']}", "%Y-%m-%d %H:%M")

        is_daytime = sunrise.time() <= forecast_time.time() <= sunset.time()
        entry_with_daytime = entry.copy()
        entry_with_daytime['forecast_isDaytime'] = is_daytime
        if forecast_time > local_now:
            upcoming_weather.append(entry_with_daytime)
        if len(upcoming_weather) == 6: # get 6 data point for the chart, it can be any number
            break
        
    print('after extract only 6'+ str(upcoming_weather))
    print(upcoming_weather)
    return upcoming_weather # return data to app.py