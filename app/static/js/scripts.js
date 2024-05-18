document.addEventListener("DOMContentLoaded", function() {
    const flashMessageContainer = document.getElementById("flash-message-container");
    if (flashMessageContainer) {
        setTimeout(() => {
            flashMessageContainer.style.display = "none";
        }, 5000); // Hide after 5 seconds
    }

    // Check if there's a message in session storage
    let message = sessionStorage.getItem('message');
    if (message) {
        // Clear previous flash messages
        document.querySelectorAll('.flash-message').forEach(el => el.remove());

        // Create a new flash message element
        const flashMessageContainer = document.createElement('div');
        flashMessageContainer.className = 'flash-message flash-success'; // or another category
        flashMessageContainer.textContent = message;
        
        // Add the flash message to the body or a specific container
        document.body.appendChild(flashMessageContainer);
        
        // Remove the message from session storage after displaying it
        sessionStorage.removeItem('message');

        // Hide the flash message after a delay
        setTimeout(() => {
            flashMessageContainer.style.display = 'none';
        }, 5000);
    }
});
