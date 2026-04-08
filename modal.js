document.addEventListener('DOMContentLoaded', () => {
    const sitrepModal = document.getElementById('sitrep-modal');
    if (!sitrepModal) return;

    let lastFocusedElement;

    const openModal = (e) => {
        if (e) e.preventDefault();
        lastFocusedElement = document.activeElement;
        sitrepModal.style.display = 'flex';

        // Focus the close button or modal content for screen readers and keyboard users
        const closeBtn = document.getElementById('close-sitrep');
        if (closeBtn) closeBtn.focus();
    };

    const closeModal = () => {
        sitrepModal.style.display = 'none';
        if (lastFocusedElement) {
            lastFocusedElement.focus();
        }
    };

    // Open modal
    const btns = document.querySelectorAll('#sitrep-btn');
    btns.forEach(btn => {
        btn.addEventListener('click', openModal);
    });

    // Close modal via button
    const closeBtn = document.getElementById('close-sitrep');
    if (closeBtn) {
        closeBtn.addEventListener('click', closeModal);
    }

    // Close modal via Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && sitrepModal.style.display === 'flex') {
            closeModal();
        }
    });

    // Close modal via outside click
    sitrepModal.addEventListener('click', (e) => {
        if (e.target === sitrepModal) {
            closeModal();
        }
    });
});
