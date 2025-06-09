# Full Stack Weather App

![Weather App Screenshot](screenshot.png)

Welcome to my first programming side project — a full-stack Weather App built with Python and Flask.  
This web application displays the current weather and a upcoming forecast weather for any location using the OpenWeatherMap API.  
It includes a clean and responsive interface with the following key features:

- Weather-based background videos that change with current weather conditions
- Geolocation support to get the weather at your current location
- An interactive line chart showing 3-hour interval temperature forecasts with weather icons
- Weather icons that change based on weather conditions and whether it's day or night


## Technologies Used

This project was built using the following technologies: 

- Python
- Flask
- HTML5 & CSS3
- Jinja2
- JavaScript
- OpenWeatherMap API
- OpenStreetMap Nominatim
- Geolocation API


## Setup & Installation

1. Clone the Repository
```bash
git clone https://github.com/LEE-Kwan-Chak/Weather-App.git
cd Weather App
```

2. Create a Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Get API key from OpenWeatherMap
- Sign up at https://openweathermap.org/api
- Copy your API key.

5. Set up the Environment Variable
Create a .env file in the root directory and add your API keys:
API_KEY = your_api_key_here

6. Run the Application
```bash
python app.py
```

7. Visit in Your Browser
- Open http://127.0.0.1:5000 to view the app.

## Live Demo

Check out the live app here: [My Weather App](https://leekc330.pythonanywhere.com/)


## License 

This project is licensed under the [MIT License](LICENSE).  
You are free to use, modify, and distribute this software with attribution.