const weatherVideos = {
  Clear: '/static/videos/clear.mp4',
  Clouds: '/static/videos/clouds.mp4',
  Rain: '/static/videos/rain.mp4',
  Thunderstorm: '/static/videos/thunderstorm.mp4',
  Snow: '/static/videos/snow.mp4',
  Drizzle: '/static/videos/drizzle.mp4',
  Mist: '/static/videos/mist.mp4',
  Default: '/static/videos/clear.mp4'
};


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

