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
            const img = document.createElement('img');
            img.src = e.target.result;
            img.height = 150; // Set image height
            img.width = 150;  // Set image width
            document.querySelector('.profile-container').insertBefore(img, document.querySelector('.profile-container').children[1]); // Insert before the upload button
        };
        reader.readAsDataURL(file);
    }
});

