document.addEventListener("DOMContentLoaded", () => {
    // Handle quantity increment and decrement
    document.querySelectorAll(".quantity-box").forEach(box => {
        const display = box.querySelector(".quantity-display");

        box.querySelector("[data-action='increase']").addEventListener("click", () => {
            display.textContent = parseInt(display.textContent, 10) + 1;
        });

        box.querySelector("[data-action='decrease']").addEventListener("click", () => {
            const current = parseInt(display.textContent, 10);
            if (current > 1) display.textContent = current - 1;
        });
    });

    // Redirect to buy page with quantity in the URL
    document.querySelectorAll(".redirect-buy").forEach(button => {
        button.addEventListener("click", () => {
            const productSlug = button.getAttribute("data-product-slug");
            const quantity = parseInt(
                button.parentElement.querySelector(".quantity-display").textContent,
                10
            );

            // Redirect to the product detail page with quantity in the URL
            window.location.href = `/products/${productSlug}/${quantity}/`;
        });
    });
});
