// Show modal on form submission
        function showModal(event) {
            event.preventDefault(); // Prevent form submission for demo purposes
            document.getElementById('successModal').style.display = 'flex';
        }

        // Close the modal
        function closeModal() {
            document.getElementById('successModal').style.display = 'none';
        }

        // Return button function
        function goBack() {
            window.history.back();
        }
