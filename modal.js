document.addEventListener('DOMContentLoaded', () => {
    const sitrepModal = document.getElementById('sitrep-modal');
    if (!sitrepModal) return;

    // Open modal
    const btns = document.querySelectorAll('#sitrep-btn');
    btns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            sitrepModal.style.display = 'flex';
        });
    });

    // Close modal
    const closeBtn = document.getElementById('close-sitrep');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            sitrepModal.style.display = 'none';
        });
    }
});
