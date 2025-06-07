import requests
from dotenv import load_dotenv
import os
from datetime import datetime
API_KEY = os.getenv('API_KEY')

def get_current_weather(city= None, lat = None, lon = None):

    if city:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    elif lat and lon:
        url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'


    try:
        res = requests.get(url)
        current_data = res.json()
        state = current_data['cod']

        if state != 200:
            return None, state
        
        timezone_offset_seconds = current_data['timezone']
        last_update = datetime.utcfromtimestamp(current_data['dt'] + timezone_offset_seconds).strftime('%H:%M')

        current_weather = {
            'city' : current_data['name'],
            'temperature' : round(current_data['main']['temp'],1),
            'weather_main' : current_data['weather'][0]['main'],
            'description': current_data['weather'][0]['description'].capitalize(),
            'humidity': current_data['main']['humidity'],
            'wind_speed': round(current_data['wind']['speed']*3.6),
            'timezone': current_data['timezone'],
            'dt': current_data['dt'],
            'last_update': last_update,
            'local_date_formatted': datetime.utcfromtimestamp(current_data['dt'] + current_data['timezone']).strftime('%a, %b %d'),
            'is_daytime': current_data['dt'] >= current_data['sys']['sunrise'] and current_data['dt'] < current_data['sys']['sunset']
        }

        return current_weather,state
    except requests.RequestException as e:
        print(f"Error fetching current weather: {e}")
        return None, 'error'

def get_forecast_weather(city= None, lat = None, lon = None):
    if city:
        forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
    elif lat and lon:
        forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'


    try:
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()
        state = int(forecast_data['cod'])

        if state != 200:
            print(f"API Error (forecast): {forecast_data.get('message', 'Unknown error')}")
            return None, state

        forecast_list = []
        daily_data = {}
        three_hourly_data = []
        day = 0

        for data in forecast_data['list']:
            #Group data by date in daily_data
            entry_datetime = datetime.strptime(data['dt_txt'], '%Y-%m-%d %H:%M:%S')
            entry_date = entry_datetime.date()
            entry_time = entry_datetime.time()

            date_str = entry_date.strftime('%Y-%m-%d')
            if date_str not in daily_data:
                daily_data[date_str] = {'temps': [], 'entries': []}
            daily_data[date_str]['temps'].append(data['main']['temp'])
            daily_data[date_str]['entries'].append({'time': entry_time, 'weather_main': data['weather'][0]['main']})
            

            # Add three hourly forecast data into three_hourly_data
            dt_txt = data['dt_txt']  # e.g., "2025-05-27 15:00:00"
            entry_datetime = datetime.strptime(dt_txt, '%Y-%m-%d %H:%M:%S')
            three_hourly_data.append({
                'time': entry_datetime.strftime('%H:%M'),
                'date': entry_datetime.strftime('%Y-%m-%d'),
                'temperature': round(data['main']['temp'], 1),
                'weather_main': data['weather'][0]['main'],
            })

        # Get next five day forecast data
        for date_str in sorted(daily_data.keys()):
            temps = daily_data[date_str]['temps']
            entries = daily_data[date_str]['entries']
            min_temp = round(min(temps))
            max_temp = round(max(temps))
            weather_main = entries[0]['weather_main']
            for entry in entries:
                if 9 <= entry['time'].hour <= 15:
                    weather_main = entry['weather_main']
                    break
            entry_date = datetime.strptime(date_str, '%Y-%m-%d')
            forecast_list.append({
                'date_formatted': entry_date.strftime('%a, %b %d'),
                'min_temp': min_temp,
                'max_temp': max_temp,
                'weather_main': weather_main
            })

        print(three_hourly_data)

        return forecast_list, state, three_hourly_data
    except requests.RequestException as e:
        print(f"Error fetching forecast weather: {e}")
        return None, 'error', None
