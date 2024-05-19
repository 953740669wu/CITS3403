let catSlideIndex = 1;
let dogSlideIndex = 1;
let catTimer;
let dogTimer;

showSlides(catSlideIndex, 'cat');
showSlides(dogSlideIndex, 'dog');

function plusSlides(n, type) {
    if (type === 'cat') {
        clearInterval(catTimer);
        showSlides(catSlideIndex += n, 'cat');
        catTimer = setInterval(() => showSlides(catSlideIndex += 1, 'cat'), 3000);
    } else if (type === 'dog') {
        clearInterval(dogTimer);
        showSlides(dogSlideIndex += n, 'dog');
        dogTimer = setInterval(() => showSlides(dogSlideIndex += 1, 'dog'), 3000);
    }
}

function currentSlide(n, type) {
    if (type === 'cat') {
        clearInterval(catTimer);
        showSlides(catSlideIndex = n, 'cat');
        catTimer = setInterval(() => showSlides(catSlideIndex += 1, 'cat'), 3000);
    } else if (type === 'dog') {
        clearInterval(dogTimer);
        showSlides(dogSlideIndex = n, 'dog');
        dogTimer = setInterval(() => showSlides(dogSlideIndex += 1, 'dog'), 3000);
    }
}

function showSlides(n, type) {
    let i;
    let slides, texts, dots;
    
    if (type === 'cat') {
        slides = document.querySelectorAll("#cat-screen ul li");
        texts = document.querySelectorAll("#cat-text .text-slide");
        dots = document.querySelectorAll(".cat-dots .dot");

        if (n > slides.length) { catSlideIndex = 1 }
        if (n < 1) { catSlideIndex = slides.length }
    } else if (type === 'dog') {
        slides = document.querySelectorAll("#dog-screen ul li");
        texts = document.querySelectorAll("#dog-text .text-slide");
        dots = document.querySelectorAll(".dog-dots .dot");

        if (n > slides.length) { dogSlideIndex = 1 }
        if (n < 1) { dogSlideIndex = slides.length }
    }

    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
        texts[i].classList.remove("active-text");
    }

    for (i = 0; i < dots.length; i++) {
        dots[i].classList.remove("active");
    }

    if (type === 'cat') {
        slides[catSlideIndex - 1].style.display = "block";
        texts[catSlideIndex - 1].classList.add("active-text");
        dots[catSlideIndex - 1].classList.add("active");
    } else if (type === 'dog') {
        slides[dogSlideIndex - 1].style.display = "block";
        texts[dogSlideIndex - 1].classList.add("active-text");
        dots[dogSlideIndex - 1].classList.add("active");
    }
}

// Initialize timers
catTimer = setInterval(() => showSlides(catSlideIndex += 1, 'cat'), 3000);
dogTimer = setInterval(() => showSlides(dogSlideIndex += 1, 'dog'), 3000);
