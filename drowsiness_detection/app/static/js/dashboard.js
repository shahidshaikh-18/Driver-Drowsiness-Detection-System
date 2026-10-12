document.addEventListener("DOMContentLoaded", function() {
    const startDetectionBtn = document.getElementById("startDetectionBtn");

    // Handle Start Detection button click
    startDetectionBtn.addEventListener("click", function() {
        // Perform the action to start detection by calling the Flask route via JavaScript
        fetch('/start-detection', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            // Redirect to detection page without showing popup
            window.location.href = "/detection";
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while starting detection.');
        });
    });
});
