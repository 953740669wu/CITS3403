// navbar.js
document.addEventListener("DOMContentLoaded", function() {
    const usernameLink = document.querySelector(".username-link");
    if (usernameLink) {
        const originalText = usernameLink.innerText; // Store the original username text
        usernameLink.addEventListener("mouseover", function() {
            usernameLink.innerText = "Profile";
        });
        usernameLink.addEventListener("mouseout", function() {
            usernameLink.innerText = originalText; // Revert back to the original username text
        });
    }
});
