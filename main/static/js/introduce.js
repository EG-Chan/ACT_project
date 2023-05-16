const sliderDesktop = document.querySelector('.desktop');
const sliderMobile = document.querySelector('.mobile');
const itemsDesktop = document.querySelectorAll('.desktop .item');
const itemsMobile = document.querySelectorAll('.mobile .item');
const buttonLeft = document.querySelector('#left');
const buttonRight = document.querySelector('#right');

let currentIndex = 0;

//슬라이드 이동시키기
function slideTo(index) {
    if (screen.width >= 600) {
        sliderDesktop.style.transform = `translateX(calc(-${index} * (100% + 20vw)))`;
    }else{
        sliderMobile.style.transform = `translateX(calc(-${index} * (100% + 20vw)))`;
    }
    
}

buttonLeft.addEventListener("click", (e) => {
    if (screen.width >= 600) {
        if (currentIndex === 0) {
            currentIndex = itemsDesktop.length - 1;
        } else {
            currentIndex = currentIndex - 1;
        }
    }else{
        if (currentIndex === 0) {
            currentIndex = itemsMobile.length - 1;
        } else {
            currentIndex = currentIndex - 1;
        }
    }
    
    slideTo(currentIndex);
});

buttonRight.addEventListener("click", (e) => {
    if (screen.width >= 600) {
        if (currentIndex === itemsDesktop.length - 1) {
            currentIndex = 0;
        } else {
            currentIndex = currentIndex + 1;
        }
    }else{
        if (currentIndex === itemsMobile.length - 1) {
            currentIndex = 0;
        } else {
            currentIndex = currentIndex + 1;
        }
    }
    slideTo(currentIndex);
});

