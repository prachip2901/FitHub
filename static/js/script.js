/* ===============================
   YOGA ROUTINE PROGRESS
================================ */
const checks = document.querySelectorAll('#routineList input');

checks.forEach(check => {
  check.addEventListener('change', updateProgress);
});

function updateProgress() {
  const total = checks.length;
  const completed = [...checks].filter(c => c.checked).length;
  const percent = Math.round((completed / total) * 100);

  const bar = document.getElementById('progressFill');
  bar.style.width = percent + '%';
  bar.innerText = percent + '%';
}

/* ===============================
   MOOD FILTER LOGIC
================================ */
const videos = document.querySelectorAll('.video-card');

const moodMap = {
  stressed: ['relaxation'],
  tired: ['morning', 'relaxation'],
  energetic: ['power', 'morning'],
  all: ['morning', 'power', 'relaxation']
};

function filterMood(mood, btn) {
  document
    .querySelectorAll('.mood-buttons button')
    .forEach(b => b.classList.remove('active'));

  btn.classList.add('active');

  videos.forEach(video => {
    const type = video.dataset.type;
    video.style.display = moodMap[mood].includes(type)
      ? 'block'
      : 'none';
  });
}

/* ===============================
   VIDEO LIGHTBOX
================================ */
const lightbox = document.getElementById('lightbox');
const iframe = lightbox.querySelector('iframe');

videos.forEach(video => {
  video.addEventListener('click', () => {
    iframe.src = video.dataset.video + '?autoplay=1';
    lightbox.style.display = 'flex';
  });
});

function closeLightbox() {
  iframe.src = '';
  lightbox.style.display = 'none';
}

/* ===============================
   VIDEO CAROUSEL CONTROLS
================================ */
const carousel = document.getElementById('videoCarousel');

function scrollCarousel(direction) {
  carousel.scrollBy({
    left: direction * 300,
    behavior: 'smooth'
  });
}

/* ===============================
   AUTO SCROLL (SMOOTH EFFECT)
================================ */
let scrollDir = 1;

setInterval(() => {
  carousel.scrollLeft += scrollDir;

  if (
    carousel.scrollLeft <= 0 ||
    carousel.scrollLeft >= carousel.scrollWidth - carousel.clientWidth
  ) {
    scrollDir *= -1;
  }
}, 25);
