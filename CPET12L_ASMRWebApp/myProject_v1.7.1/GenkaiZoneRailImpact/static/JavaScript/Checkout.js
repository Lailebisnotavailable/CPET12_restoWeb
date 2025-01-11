console.log("JavaScript is working");
document.addEventListener('DOMContentLoaded', function() {
    const addToCartButton = document.querySelector('.add-to-cart-btn');
    
    // Ensure the button exists on the page before adding event listener
    if (addToCartButton) {
        addToCartButton.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent form submission

            const foodId = this.getAttribute('data-food-id');
            const userId = this.getAttribute('data-user-id');

            if (!userId) {
                alert('Please log in first!');
                window.location.href = '/LogIn';  // Redirect to login if not logged in
                return;
            }

            // Send AJAX POST request to add item to the cart
            fetch('/add-to-cart/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value  // CSRF token for security
                },
                body: JSON.stringify({
                    food_id: foodId,
                    user_id: userId,
                })
            })

            .then(response => response.json())
            .then(data => {
                if (data.exists) {
                    alert(data.message);  // Item already in cart, quantity updated
                } else {
                    alert(data.message);  // Item added to the cart
                }
            })
        });
    }
});
