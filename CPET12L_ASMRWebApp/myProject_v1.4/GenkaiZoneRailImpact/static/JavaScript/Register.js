// Function to toggle the visibility of a password input field
function togglePasswordVisibility(inputId) {
    const inputField = document.getElementById(inputId);
    const currentType = inputField.getAttribute('type');
    inputField.setAttribute('type', currentType === 'password' ? 'text' : 'password');
}

// Function to toggle the custom question input visibility based on dropdown selection
function toggleCustomQuestion() {
    const dropdown = document.getElementById("sec-question");
    const customQuestionDiv = document.getElementById("custom-question-div");

    // Show the custom question input if "Custom Question" is selected
    customQuestionDiv.style.display = dropdown.value === "custom" ? "block" : "none";
}

// Function to set the maximum date for the birthday input to today
function setMaxDate() {
    const today = new Date();
    const formattedDate = today.toISOString().split('T')[0]; // Format as YYYY-MM-DD
    document.getElementById('birthday').setAttribute('max', formattedDate);
}

// Function to validate passwords and display error messages
function validatePasswords(event) {
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm-password").value;
    const errorMessageDiv = document.getElementById("error-message");

    // Clear previous error messages
    errorMessageDiv.innerHTML = "";

    let hasError = false;

    // Check if passwords match
    if (password !== confirmPassword) {
        hasError = true;
        // Display error message
        errorMessageDiv.innerHTML += "<span style='color: red;'>Passwords didn't match.</span><br>";
    }

    // Check for any server-side validation error passed in from Django
    const emailError = "{{ error_message }}"; // This will need to be replaced by Django when rendering
    if (emailError) {
        hasError = true;
        errorMessageDiv.innerHTML += `<span style='color: red;'>${emailError}</span><br>`;
    }

    // Prevent form submission if there's any error
    if (hasError) {
        event.preventDefault();
    }
}

// Set the maximum date on the birthday field when the page loads
window.onload = setMaxDate;
