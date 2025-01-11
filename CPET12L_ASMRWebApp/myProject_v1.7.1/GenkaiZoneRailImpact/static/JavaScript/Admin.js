document.addEventListener('DOMContentLoaded', function () {
    // Initialize Bootstrap Tabs
    const tabs = document.querySelectorAll('[data-bs-toggle="tab"]');
    tabs.forEach(tab => {
        tab.addEventListener('shown.bs.tab', function (e) {
            console.log(`Activated Tab: ${e.target.id}`);
        });
    });

    // Toggle dropdown and save state
    const toggleButton = document.getElementById('toggleButton');
    const dishesTable = document.getElementById('dishesTable');
    const arrowIndicator = document.getElementById('arrowIndicator');
    const dropdownState = localStorage.getItem('dropdownState');
    const scrollPosition = localStorage.getItem('scrollPosition');

    if (dropdownState === 'open') {
        dishesTable.style.display = 'table';
        arrowIndicator.textContent = '↓';
    } else {
        dishesTable.style.display = 'none';
        arrowIndicator.textContent = '→';
    }

    if (scrollPosition) {
        window.scrollTo(0, scrollPosition);
    }

    toggleButton.addEventListener('click', function () {
        if (dishesTable.style.display === 'none') {
            dishesTable.style.display = 'table';
            arrowIndicator.textContent = '↓';
            localStorage.setItem('dropdownState', 'open');
        } else {
            dishesTable.style.display = 'none';
            arrowIndicator.textContent = '→';
            localStorage.setItem('dropdownState', 'closed');
        }
    });

    window.addEventListener('scroll', function () {
        localStorage.setItem('scrollPosition', window.scrollY);
    });

    // Sorting functionality
    document.querySelectorAll('.sortable').forEach((th) => {
        th.addEventListener('click', function () {
            const table = th.closest('table');
            const rows = Array.from(table.querySelectorAll('tbody tr'));
            const index = Array.from(th.parentNode.children).indexOf(th);
            const isAscending = th.classList.contains('asc');
            const columnType = th.getAttribute('data-column');

            rows.sort((rowA, rowB) => {
                const cellA = rowA.cells[index].textContent.trim();
                const cellB = rowB.cells[index].textContent.trim();

                if (columnType === 'price') {
                    const priceA = parseFloat(cellA.replace(/[^\d.-]/g, ''));
                    const priceB = parseFloat(cellB.replace(/[^\d.-]/g, ''));
                    return isAscending ? priceA - priceB : priceB - priceA;
                } else if (columnType === 'name' || columnType === 'category') {
                    return isAscending ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
                }

                return 0;
            });

            rows.forEach(row => table.querySelector('tbody').appendChild(row));
            th.classList.toggle('asc', !isAscending);
            th.classList.toggle('desc', isAscending);
        });
    });
})

// Add dish prompt cccccccccccccccccccc
function confirmAddDish(event) {
    const userConfirmed = confirm("Are you sure you want to add this dish?");
    if (!userConfirmed) {
        // Prevent form submission if the user cancels
        event.preventDefault();
        alert("You didn't add the dish.");
    } else {
        console.log("Dish added!"); // Debug log
    }
}
