const questionImg = document.querySelector('.img_act');
const explantionBar = document.querySelector('.explanation');
const checkBar = document.querySelector('.non_explanation');

explantionBar.style.display = 'none';
checkBar.style.display = 'block';

// questionImg.addEventListener('mousemove', () => {
//   explantionBar.style.display = 'block';
//   checkBar.style.display = 'none';
// });

// questionImg.addEventListener('mouseleave', () => {
//   explantionBar.style.display = 'none';
//   checkBar.style.display = 'block';
// });

let isExplanationVisible = false;
questionImg.addEventListener('click', () => {
  if (isExplanationVisible) {
    explantionBar.style.display = 'none';
    checkBar.style.display = 'block';
  } else {
    explantionBar.style.display = 'block';
    checkBar.style.display = 'none';
  }
  isExplanationVisible = !isExplanationVisible;
});