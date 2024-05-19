var catIndex = 1;
showSlides(catIndex, 'cat');

var dogIndex = 1;
showSlides(dogIndex, 'dog');

// Next/previous controls
function plusSlides(n, type) {
    if (type === 'cat') {
        showSlides(catIndex += n, 'cat');
    } else if (type === 'dog') {
        showSlides(dogIndex += n, 'dog');
    }
}

function currentSlide(n, type) {
    if (type === 'cat') {
        showSlides(catIndex = n, 'cat');
    } else if (type === 'dog') {
        showSlides(dogIndex = n, 'dog');
    }
}

function showSlides(n, type) {
    var i;
    var slides, dots;
    if (type === 'cat') {
        slides = document.querySelectorAll('#cat-screen ul li');
        textSlides = document.querySelectorAll('#cat-text .text-slide');
        dots = document.querySelectorAll('#cat-slideshow .dot');
    } else if (type === 'dog') {
        slides = document.querySelectorAll('#dog-screen ul li');
        textSlides = document.querySelectorAll('#dog-text .text-slide');
        dots = document.querySelectorAll('#dog-slideshow .dot');
    }

    if (n > slides.length) {
        if (type === 'cat') {
            catIndex = 1;
        } else if (type === 'dog') {
            dogIndex = 1;
        }
    }
    if (n < 1) {
        if (type === 'cat') {
            catIndex = slides.length;
        } else if (type === 'dog') {
            dogIndex = slides.length;
        }
    }

    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = 'none';
        textSlides[i].classList.remove('active-text');
    }

    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(' active', '');
    }

    if (type === 'cat') {
        slides[catIndex - 1].style.display = 'block';
        textSlides[catIndex - 1].classList.add('active-text');
        dots[catIndex - 1].className += ' active';
    } else if (type === 'dog') {
        slides[dogIndex - 1].style.display = 'block';
        textSlides[dogIndex - 1].classList.add('active-text');
        dots[dogIndex - 1].className += ' active';
    }
}
