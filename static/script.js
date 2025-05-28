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
});