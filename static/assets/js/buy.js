
// Flavor Picker Functionality
const flavorPickers = document.querySelectorAll('.FlavorPicker');
const selectedFlavor = document.getElementById('SelectedFlavor');
const selectedFlavorInTable = document.getElementById('SelectedFlavorInTable');
const priceSpan = document.getElementById('Num'); // For updating the price
const quantityDisplay = document.getElementById('Quant'); // Quantity display

// Toggle functionality for ingredients and additional info sections
document.addEventListener("DOMContentLoaded", function () {
    const toggleButtons = document.querySelectorAll(".toggle-button");

    toggleButtons.forEach(button => {
        button.addEventListener("click", function () {
            const textDiv = this.nextElementSibling;
            const icon = this.querySelector(".toggle-icon");

            // Toggle visibility of the corresponding text
            if (textDiv.style.display === "block") {
                textDiv.style.display = "none";
                icon.style.transform = "rotate(0deg)"; // Reset icon to >
            } else {
                textDiv.style.display = "block";
                icon.style.transform = "rotate(90deg)"; // Rotate icon to point downward
            }
        });
    });
});

function addToCart(productId, flavorId, quantity) {
    const url = '/cart/add/';
    const data = {
        id: productId,
        flavor: flavorId,
        quantity: quantity // Include quantity in the request
    };

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify(data)
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                console.log(data.message); // Log success message
                alert(`${data.message}`);
            } else if (data.error) {
                console.error(data.error); // Log any errors
                alert(`Error: ${data.error}`);
            }
        })
        .catch(error => console.error(`Fetch error: ${error}`));
}


flavorPickers.forEach(picker => {
    picker.addEventListener('click', () => {
        // Remove active class from all pickers
        flavorPickers.forEach(p => p.classList.remove('active'));

        // Add active class to the clicked picker
        picker.classList.add('active');

        // Get flavor name and price from dataset
        const flavor = picker.dataset.flavorName; // Flavor name
        const price = picker.dataset.price; // Flavor price

        // Update flavor name in display and table
        selectedFlavor.textContent = flavor;
        selectedFlavorInTable.textContent = flavor;

        // Update price in the #Num span
        priceSpan.textContent = price;
    });
});

// Handle quantity increment/decrement
document.getElementById('Plus').addEventListener('click', () => {
    let quantity = parseInt(quantityDisplay.textContent, 10);
    quantityDisplay.textContent = quantity + 1; // Increment quantity
});

document.getElementById('Minus').addEventListener('click', () => {
    let quantity = parseInt(quantityDisplay.textContent, 10);
    if (quantity > 1) {
        quantityDisplay.textContent = quantity - 1; // Decrement quantity
    }
});

// Function to get CSRF token for AJAX requests
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Add to Cart Functionality
document.getElementById('addToCart').addEventListener('click', () => {
    const productId = document.getElementById('addToCart').value; // Get the product ID
    const selectedFlavorPicker = document.querySelector('.FlavorPicker.active');
    const flavorId = selectedFlavorPicker ? selectedFlavorPicker.dataset.flavorId : null;

    if (!flavorId) {
        alert('Please select a flavor before adding to cart!');
        return;
    }

    const quantity = parseInt(quantityDisplay.textContent, 10); // Get selected quantity

    addToCart(productId, flavorId, quantity);
});


