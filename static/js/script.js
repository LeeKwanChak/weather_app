const weatherVideos = {
  Clear: '/static/videos/clear.mp4',
  Clouds: '/static/videos/clouds.mp4',
  Night: '/static/videos/night.mp4',
  Rain: '/static/videos/rain.mp4',
  Thunderstorm: '/static/videos/rain.mp4',
  Snow: '/static/videos/snow.mp4',
  Drizzle: '/static/videos/rain.mp4',
  Mist: '/static/videos/mist.mp4',
  Default: '/static/videos/clear.mp4'
};


const video = document.getElementById('background-video');
const source = document.getElementById('video-source');
const currentWeather = document.body.getAttribute('data-current-weather');
const isDaytime = document.body.getAttribute('data-is-daytime') === 'true';


let initialWeatherKey = currentWeather;
if ((currentWeather === 'Clouds' || currentWeather === 'Clear') && !isDaytime) {
  initialWeatherKey = 'Night';
}
const initialVideoSrc = weatherVideos[initialWeatherKey] || weatherVideos.Default;
if (source.getAttribute('src') !== initialVideoSrc) {
  source.setAttribute('src', initialVideoSrc);
  video.load();
  video.play();
}



document.addEventListener('DOMContentLoaded', () => {
  const forecastCards = document.querySelectorAll('.forecast-card');
  const video = document.getElementById('background-video');
  const source = document.getElementById('video-source');

  forecastCards.forEach(card => {
    // change background video if click the forecast card
    card.addEventListener('click', () => {
      const condition = card.getAttribute('data-weather') || card.querySelector('.condition').textContent;
      const videoSrc = weatherVideos[condition] || weatherVideos.Default;

      if (source.getAttribute('src') !== videoSrc) {
        source.setAttribute('src', videoSrc);
        video.load();
        video.play();
      }
    });
  });


  const locationButton = document.getElementById('detect-location')
  if (locationButton) {
    locationButton.addEventListener('click', () => {
      if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
      }else{
        alert("Error");
      }
    })
  }


  function successCallback(position){
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    // reverse lat and lon to the location name, openstreetmap is perform better than openweathermap in this case.
    fetch(`https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lon}`)
    .then(response => response.json())
    .then(data => {
    const location = data.address.neighbourhood || data.address.city
  
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/';
    
    const locationInput = document.createElement('input');
    locationInput.type = 'hidden';
    locationInput.name = 'location';
    locationInput.value = location;

    const latInput = document.createElement('input');
    latInput.type = 'hidden';
    latInput.name = 'lat';
    latInput.value = lat;

    const lonInput = document.createElement('input');
    lonInput.type = 'hidden';
    lonInput.name = 'lon';
    lonInput.value = lon;

    form.appendChild(locationInput);
    form.appendChild(latInput);
    form.appendChild(lonInput);
    document.body.appendChild(form);
    form.submit(); // give the data to the backend
    });
  }

  function errorCallback(error) {
    alert("Unable to retrieve your location. Please allow location access.");
  }


  if (typeof forecastData !== 'undefined' && forecastData.length > 0) {
    const labels = forecastData.map(entry => entry.time);
    const temperatures = forecastData.map(entry => entry.temperature);

    const weatherConditions = forecastData.map(entry => {
      const condition = entry.weather_main.toLowerCase();
      const isDaytime = entry.forecast_isDaytime;

      // determine using day or night icon
      if (condition === 'clouds' && !isDaytime) {
        return 'cloudy-night';
      } else if (condition === 'clear' && !isDaytime) {
        return 'clear-night';
      }
      return condition;
    });

    const ctx = document.getElementById('forecastChart').getContext('2d');

    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(120, 180, 255, 0.4)');
    gradient.addColorStop(1, 'rgba(120, 180, 255, 0.05)');

    const iconMap = {
      'clear': '/static/weather-icon/day.svg',
      'clear-night': '/static/weather-icon/night.svg',
      'clouds': '/static/weather-icon/cloudy-day-1.svg',
      'cloudy-night': '/static/weather-icon/cloudy-night-1.svg',
      'rain': '/static/weather-icon/rainy.svg',
      'drizzle': '/static/weather-icon/drizzle.svg',
      'snow': '/static/weather-icon/snow.svg',
      'thunderstorm': '/static/weather-icon/thunderstorm.svg',
      'mist': '/static/weather-icon/mist.svg',
      'default': '/static/weather-icon/clear.svg'
    };

    // Preload the icon, avoiding the delay
    const preloadedIcons = {};
    Object.entries(iconMap).forEach(([key, src]) => {
      const img = new Image();
      img.src = src;
      preloadedIcons[key] = img;
    });

    // Insert weather icon above the temperature
    const weatherIconPlugin = {
      id: 'weatherIconPlugin',
      afterDraw: (chart) => {
        const ctx = chart.ctx;
        const meta = chart.getDatasetMeta(0);

        ctx.save();
        meta.data.forEach((point, index) => {
          const x = point.x;
          const y = point.y;
          const weather = weatherConditions[index];
          const icon = preloadedIcons[weather] || preloadedIcons['default'];

          if (icon.complete) {
            const size = 40;
            ctx.drawImage(icon, x - size / 2, y - size - 25, size, size);
          }
        });
        ctx.restore();
      }
    };

    // Chart for showing the upcoming weather
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Temperature (°C)',
          data: temperatures,
          fill: true,
          tension: 0.4,
          borderColor: 'rgba(120, 180, 255, 1)',
          backgroundColor: gradient,
          pointBackgroundColor: 'white',
          pointBorderColor: 'rgba(120, 180, 255, 1)',
          pointRadius: 4
        }],
        weatherConditions: weatherConditions
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          datalabels: {
            color: '#ffffff',
            align: 'top',
            anchor: 'end',
            font: { size: 14, weight: 'bold' },
            formatter: value => `${value}°`
          }
        },
        scales: {
          y: {
            display: false,
            min: Math.min(...temperatures) - 3,
            max: Math.max(...temperatures) + 3,
            grid: { display: false }
          },
          x: {
            grid: { display: false },
            ticks: {
              color: '#ffffff',
              font: { size: 14, weight: '500' }
            }
          }
        }
      },
      plugins: [ChartDataLabels, weatherIconPlugin]
    });
  }
});


