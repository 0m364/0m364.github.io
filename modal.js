document.addEventListener('DOMContentLoaded', () => {
    const sitrepModal = document.getElementById('sitrep-modal');
    if (!sitrepModal) return;

    let lastFocusedElement;

const openModal = (e) => {
        if (e) e.preventDefault();
        lastFocusedElement = document.activeElement;
        sitrepModal.style.display = 'flex';

        // Make content scrollable for keyboard users
        const contentContainer = sitrepModal.querySelector('.sitrep-modal-content');
        if (contentContainer) {
            contentContainer.setAttribute('tabindex', '0');
        }

        // Focus the content container or close button
        if (contentContainer) {
            contentContainer.focus();
        } else {
            const closeBtn = document.getElementById('close-sitrep');
            if (closeBtn) closeBtn.focus();
        }
    };

    const closeModal = () => {
        sitrepModal.style.display = 'none';
        if (lastFocusedElement) {
            lastFocusedElement.focus();
        }
    };

    // Focus Trap
    sitrepModal.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            const focusableElements = sitrepModal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
            const firstElement = focusableElements[0];
            const lastElement = focusableElements[focusableElements.length - 1];

            if (e.shiftKey) { // Shift + Tab
                if (document.activeElement === firstElement) {
                    lastElement.focus();
                    e.preventDefault();
                }
            } else { // Tab
                if (document.activeElement === lastElement) {
                    firstElement.focus();
                    e.preventDefault();
                }
            }
        }
    });

    // Open modal
    const btns = document.querySelectorAll('#sitrep-btn');
    btns.forEach(btn => {
        btn.addEventListener('click', openModal);
        btn.addEventListener('keydown', (e) => {
            if (e.key === ' ' || e.key === 'Spacebar') {
                e.preventDefault();
                openModal(e);
            }
        });
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
