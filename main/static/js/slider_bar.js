let currentSlide = 0;
const slides = document.querySelectorAll('.ooooo');
const slideWidth = slides[0].offsetWidth;

function moveToSlide(n) {
  currentSlide = (n + slides.length) % slides.length;
  slides[0].style.marginLeft = -currentSlide * slideWidth + 'px';
}

document.querySelector('.next_button').addEventListener('click', () => moveToSlide(currentSlide + 5));
document.querySelector('.prev_button').addEventListener('click', () => moveToSlide(currentSlide - 5));