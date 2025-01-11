document.addEventListener('DOMContentLoaded', function() {
    // Select all remove buttons
    const removeButtons = document.querySelectorAll('.remove-btn');
    
    // Loop through each remove button and attach an event listener
    removeButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent form submission
            // Get the row that contains the button
            const row = button.closest('tr');
            var userConfirmed = confirm("Are you sure you want to perform this action?");
            if (userConfirmed) {
            // Send AJAX POST request to update the cart (adjust the payload as needed)
                fetch('/update_user_cart', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value  // CSRF token for security
                    },
                    body: JSON.stringify({
                        cart_id: row.dataset.itemId // Pass the item ID (or any other identifier)
                    })
                })
                .then(response => response.json()) // Assuming the response is JSON
                .then(data => {
                        alert("Item removed from cart");

                        // Remove the row from the table after successful response
                        row.remove();
                        
                        // Update the total price
                        updateTotal();

                        // Check if the cart is empty and update the view
                        checkIfCartIsEmpty();
                
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert("There was an issue removing the item.");
                });
            } else {
            // User clicked "No"
            }
        });
    });
});
