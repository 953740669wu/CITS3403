$(document).ready(function() {
    $('form').on('submit', function(event) {
        event.preventDefault();

        const form = $(this);
        const actionUrl = form.attr('action');
        const formData = form.serialize();

        $.post(actionUrl, formData, function(data) {
            if (data.redirect) {
                sessionStorage.setItem('message', data.message);
                window.location.href = data.redirect;
            }
        });
    });

    // Check if there's a message in session storage
    let message = sessionStorage.getItem('message');
    if (message) {
        $('#flash-content').text(message);
        $('#flash-message').show();
        // Remove the message from session storage after displaying it
        sessionStorage.removeItem('message');
    }

    // Close the pop-up when the close button is clicked
    $('#close-popup').on('click', function() {
        $('#flash-message').hide();
    });
});
