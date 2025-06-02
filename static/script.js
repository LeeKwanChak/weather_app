const weatherVideos = {
  Clear: '/static/videos/clear.mp4',
  Clouds: '/static/videos/clouds.mp4',
  Night: '/static/videos/night.mp4',
  Rain: '/static/videos/rain.mp4',
  Thunderstorm: '/static/videos/thunderstorm.mp4',
  Snow: '/static/videos/snow.mp4',
  Drizzle: '/static/videos/drizzle.mp4',
  Mist: '/static/videos/mist.mp4',
  Default: '/static/videos/clear.mp4'
};

const video = document.getElementById('background-video');
const source = document.getElementById('video-source');

// Set background video on initial load based on current weather
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


// change background video on forecast card
document.addEventListener('DOMContentLoaded', () => {
  const forecastCards = document.querySelectorAll('.forecast-card');
  const video = document.getElementById('background-video');
  const source = document.getElementById('video-source');

  forecastCards.forEach(card => {
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
    form.submit();
    });
  }

    function errorCallback(error) {
    alert("Unable to retrieve your location. Please allow location access.");
  }

});


document.addEventListener("DOMContentLoaded", () => {
  if (typeof forecastData !== 'undefined') {
    const labels = forecastData.map(entry => entry.time);
    const temperatures = forecastData.map(entry => entry.temperature);

    const ctx = document.getElementById('forecastChart').getContext('2d');

  const gradient = ctx.createLinearGradient(0, 0, 0, 400);
  gradient.addColorStop(0, 'rgba(120, 180, 255, 0.4)');  // soft top blue
  gradient.addColorStop(1, 'rgba(120, 180, 255, 0.05)'); // light fade at bottom

new Chart(ctx, {
  type: 'line',
  data: {
    labels: labels,
  datasets: [{
    label: 'Temperature (°C)',
    data: temperatures,
    fill: true,
    tension: 0.4,
    borderColor: 'rgba(120, 180, 255, 1)',          // soft blue line
    backgroundColor: gradient,                      // blue gradient fill
    pointBackgroundColor: 'white',
    pointBorderColor: 'rgba(120, 180, 255, 1)',
    pointRadius: 4
  }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        display: false
      },
      datalabels: {
        color: '#ffffff',
        align: 'top',
        anchor: 'end',
        font: {
          size: 14,
          weight: 'bold'
        },
        formatter: value => `${value}°`
      }
    },
    scales: {
      y: {
        display: false,
        min: Math.min(...temperatures) - 3, 
        max: Math.max(...temperatures) + 3,
        grid: {
          display: false
        }
      },
      x: {
        grid: {
          display: false
        },
        ticks: {
          color: '#ffffff',
          font: {
            size: 14,
            weight: '500'
          }
        }
      }
    }
  },
  plugins: [ChartDataLabels]  // Register the plugin
});
  }
});