# Weather app

![Weather App Screenshot](screenshot.gif)

This web application displays the current weather and the upcoming weather forecast for any location using the OpenWeatherMap API. 
It includes a clean and responsive interface with the following key features:

- Weather-based background videos that change with current weather conditions
- Geolocation support to get the weather at your current location
- An interactive line chart showing 3-hour interval temperature forecasts with weather icons
- Weather icons that change based on weather conditions and whether it's day or night


## Live Demo

Check out the live app here: [Full Stack Weather App](https://leekc330.pythonanywhere.com/)


## Technologies Used

This project was built using the following technologies: 

- Python
- Flask
- HTML5 & CSS3
- JavaScript
- OpenWeatherMap API
- OpenStreetMap Nominatim
- Geolocation API


## Setup & Installation

1. Clone the Repository
```bash
git clone https://github.com/LeeKwanChak/Full-Stack-Weather-App.git
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
    * Sign up at https://openweathermap.org/api
    * Copy your API key.

5. Set up the Environment Variable
    * Create a .env file in the root directory and add your API keys:
    * API_KEY = your_api_key_here

6. Run the Application
```bash
python app.py
```

7. Visit in Your Browser
    * Open http://127.0.0.1:5000 to view the app.


## License 

This project is licensed under the [MIT License](LICENSE).  
You are free to use, modify, and distribute this software with attribution.
