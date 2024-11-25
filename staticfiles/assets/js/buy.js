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
// Function to get the CSRF token from cookies
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
    return cookieValue;
}



document.addEventListener("DOMContentLoaded", function () {
    const addToCartButton = document.getElementById("addToCartButton");

    addToCartButton.addEventListener("click", function () {
        const slug = this.dataset.slug;
        const url = "/add_to_cart/";
        const csrftoken = getCookie("csrftoken");

        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken,
            },
            body: JSON.stringify({ slug: slug, quantity: 1 }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    alert(`${data.message}`);
                } else {
                    alert(`Error: ${data.error}`);
                }
            })
            .catch((error) => console.error("Error:", error));
    });
});
