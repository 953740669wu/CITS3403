
document.addEventListener("DOMContentLoaded", function() {
    var popup = document.getElementById('popup');
    var popupMessage = document.getElementById('popup-message');
    var popupClose = document.getElementById('popup-close');

    if (popupMessage.textContent.trim() !== "") {
        popup.classList.add('show');
        setTimeout(function() {
            popup.classList.remove('show');
        }, 3000);
    }

    popupClose.addEventListener('click', function(event) {
        event.preventDefault();
        popup.classList.remove('show');
    });
});

