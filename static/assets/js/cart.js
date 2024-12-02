document.addEventListener('DOMContentLoaded', function () {
    const quantityButtons = document.querySelectorAll('.quantity-btn');

    quantityButtons.forEach(button => {
        button.addEventListener('click', function () {
            const action = this.getAttribute('data-action');
            const itemId = this.getAttribute('data-item-id');

            fetch('/cart/update_quantity/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({
                    'item_id': itemId,
                    'action': action
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update quantity display
                    document.getElementById(`quantity-${itemId}`).textContent = data.new_quantity;

                    // Update item total price
                    document.getElementById(`item-total-${itemId}`).textContent = data.item_total_price;

                    // Update cart total price
                    document.getElementById('cart-total').textContent = data.cart_total_price;
                } else {
                    alert(data.error || 'Error updating quantity');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
