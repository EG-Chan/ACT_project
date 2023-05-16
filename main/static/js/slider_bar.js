let currentSlide = 0;
const slides = document.querySelectorAll('.ooooo');
const slideWidth = slides[0].offsetWidth;

function moveToSlide(n) {
  currentSlide = (n + slides.length) % slides.length;
  slides[0].style.marginLeft = -currentSlide * slideWidth + 'px';
}

// 5개씩 보여주기가 css에 뭔가 꼬여있는데 시간없어서 1개씩 검색으로 바꿈
if (window.matchMedia('(min-width: 600px)').matches) {
  document.querySelector('.next_button').addEventListener('click', () => moveToSlide(currentSlide + 5));
  document.querySelector('.prev_button').addEventListener('click', () => moveToSlide(currentSlide - 5));
} else {
  document.querySelector('.next_button').addEventListener('click', () => moveToSlide(currentSlide + 1));
  document.querySelector('.prev_button').addEventListener('click', () => moveToSlide(currentSlide - 1));
}
// document.querySelector('.next_button').addEventListener('click', () => moveToSlide(currentSlide + 5));
// document.querySelector('.prev_button').addEventListener('click', () => moveToSlide(currentSlide - 5));