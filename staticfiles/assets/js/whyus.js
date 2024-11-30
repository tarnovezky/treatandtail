
document.getElementById('load-more-reviews').addEventListener('click', function() {
    const button = this;
    const page = button.getAttribute('data-page');
    const url = `/load-more-reviews/?page=${page}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const carouselInner = document.querySelector('.carousel-inner .row:last-child');
            data.reviews.forEach(review => {
                const col = document.createElement('div');
                col.className = 'col-md-4';
                col.innerHTML = `
                    <div class="card mb-4 shadow-sm review-card">
                        <img src="${review.image_url}" class="card-img-top" alt="Review Image">
                        <div class="card-body">
                            <div class="top-review-info">
                                <div class="rating_block">
                                    <div class="rating_bar" style="width: ${review.rating_percentage}%;"></div>
                                    <img src="{% static 'assets/img/ratingC_corrected_border.png' %}" alt="Rating">
                                </div>
                                <div class="card-title-block">
                                    <span class="card-title">${review.name}</span>
                                </div>
                            </div>
                            <p class="card-text">${review.description}</p>
                        </div>
                    </div>`;
                carouselInner.appendChild(col);
            });
            if (!data.has_next) {
                button.remove();
            } else {
                button.setAttribute('data-page', parseInt(page) + 1);
            }
        })
        .catch(error => console.error('Error loading more reviews:', error));
});
