// Flavor Picker Functionality
const flavorPickers = document.querySelectorAll('.FlavorPicker');
const selectedFlavor = document.getElementById('SelectedFlavor');
const selectedFlavorInTable = document.getElementById('SelectedFlavorInTable');

flavorPickers.forEach(picker => {
    picker.addEventListener('click', () => {
        // Remove active class from all pickers
        flavorPickers.forEach(p => p.classList.remove('active'));

        // Add active class to the clicked picker
        picker.classList.add('active');

        // Update the flavor name in both the display and the table
        const flavor = picker.dataset.flavor;
        selectedFlavor.textContent = flavor;
        selectedFlavorInTable.textContent = flavor;
    });
});

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





function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;}

const csrftoken = getCookie('csrftoken');


document.addEventListener('click', function(event) {
    if (event.target && (event.target.classList.contains('add-to-cart-btn')
        || event.target.classList.contains('remove-from-cart-btn')
        || event.target.classList.contains('unauth'))) {

        var pid = event.target.value;
        console.log(pid); // Print the slug to console

        if (event.target.classList.contains('add-to-cart-btn')) {
            addToCart(pid);

            // Notification("Aded to Cart", 3500);

        } else if (event.target.classList.contains('remove-from-cart-btn')) {

            // removeFromCart(id);
            // Notification("Removed from Cart", 3500);

        } else if (event.target.classList.contains('unauth')) {
            // showNotification("show");
        }
    }
});

function addToCart(pid) {
    let url = '/add_to_cart/';
    let data = { id: pid };

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
        console.log(data);
    })
    .catch(error => {
        console.log(error);
    });
    console.log(pid);
    console.log("add to cart func triggered");
}
