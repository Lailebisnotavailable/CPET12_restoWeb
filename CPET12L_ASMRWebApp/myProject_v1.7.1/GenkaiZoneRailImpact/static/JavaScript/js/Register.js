// Set the maximum date on the birthday field when the page loads
window.onload = setMaxDate;

window.onload = function() {
    // Your togglePasswordVisibility function here
};

function togglePasswordVisibility(fieldId) {
    const passwordField = document.getElementById(fieldId);
    const icon = passwordField.nextElementSibling.querySelector('img'); // Find the image in the next sibling button

    // Use the pre-defined static paths for the images
    if (passwordField.type === "password") {
        passwordField.type = "text";
        icon.src = openEyeImage; // Change to visible eye icon
    } else {
        passwordField.type = "password";
        icon.src = closedEyeImage; // Change to hidden eye icon
    }
}



function validatePasswords(event) {
    const password = document.getElementById("password").value.trim();  // trim any leading/trailing spaces
    const confirmPassword = document.getElementById("confirm-password").value.trim();
    const errorMessageDiv = document.getElementById("error-message");

    // Clear previous error messages
    errorMessageDiv.innerHTML = "";

    let hasError = false;

    // Check if passwords match
    if (password !== confirmPassword) {
        hasError = true;
        errorMessageDiv.innerHTML += "<span class='error' style='color: red; font-weight: bold;'>Passwords didn't match.</span><br>";
    }

    // Prevent form submission if there's any error
    if (hasError) {
        event.preventDefault();
    }
}

function toggleCustomQuestion() {
    const dropdown = document.getElementById("sec-question");
    const customQuestionDiv = document.getElementById("custom-question-div");

    // Show the custom question input if "Custom Question" is selected, hide otherwise
    customQuestionDiv.style.display = dropdown.value === "custom" ? "block" : "none";
}

// Function to set the maximum date for the birthday input to today’s date
function setMaxDate() {
    const birthdayInput = document.getElementById("birthday");
    const today = new Date();
    const maxDate = today.toISOString().split("T")[0];
    birthdayInput.setAttribute("max", maxDate);
}

