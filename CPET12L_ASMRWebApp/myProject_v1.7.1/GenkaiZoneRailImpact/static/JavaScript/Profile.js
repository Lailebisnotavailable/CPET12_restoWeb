function enableEditing() {
    // Get all input fields in the form
    const inputs = document.querySelectorAll('#profile-form input');
    inputs.forEach(input => {
        input.removeAttribute('readonly');
        input.removeAttribute('disabled'); // Enable all inputs including password
    });

    // Specifically enable the password input
    document.getElementById('password').removeAttribute('disabled'); // Enable the password field

    // Enable the Update button
    document.querySelector('.update-btn').removeAttribute('disabled');

    // Show instruction text for contact number
    document.getElementById('contact-instruction').style.display = 'inline';
}

document.getElementById('file-input').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            // Find the current profile image element
            const currentImage = document.querySelector('.profile-container img');

            // If an image exists (the placeholder or a previous upload), remove it
            if (currentImage) {
                currentImage.remove();
            }

            // Create a new img element and set its source to the uploaded image
            const newImg = document.createElement('img');
            newImg.src = e.target.result;
            newImg.height = 150; // Set image height
            newImg.width = 150;  // Set image width

            // Insert the new image in the same place where the old image was
            document.querySelector('.profile-container').insertBefore(newImg, document.querySelector('.profile-container').children[1]);
        };
        reader.readAsDataURL(file); // Read the uploaded file as a data URL
    }
});

