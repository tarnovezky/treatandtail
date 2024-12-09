document.getElementById('submitOrder').addEventListener('click', function (event) {
    event.preventDefault(); // Prevent form default submission

    const form = document.getElementById('checkoutForm');
    const formData = new FormData(form);

    const data = {};
    formData.forEach((value, key) => {
        data[key] = value; // Convert FormData to JSON
    });

    console.log('Data being sent:', data); // Debugging: log data

    fetch("{% url 'checkout' %}", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify(data) // Send JSON payload
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert(`Order placed successfully! Order Number: ${data.order_number}`);
        } else {
            alert(`Error: ${data.message}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An unexpected error occurred.');
    });
});
