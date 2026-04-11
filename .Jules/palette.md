## 2024-05-24 - Semantic Modals and Focus Styles
**Learning:** In vanilla JavaScript and basic HTML architectures, custom modals frequently lack proper semantic roles (e.g., `role="dialog"`, `aria-modal="true"`) and often misuse `<div>` tags for interactive elements like close buttons, breaking keyboard and screen reader accessibility. Additionally, a global reset often removes default focus outlines, creating navigation issues for keyboard users.
**Action:** Always verify that interactive elements within custom modals use native interactive tags (like `<button>`) with proper `aria-labels`. Ensure dialog containers are announced correctly with ARIA attributes. Implement global `:focus-visible` styles early in the design system to ensure consistent keyboard accessibility without impacting mouse users.

## 2025-05-25 - Semantic HTML Modals and Focus Tracking
**Learning:** Vanilla JS modals often suffer from poor focus management when opened/closed. Users navigating via keyboard get "lost" when a modal closes and their focus is not returned to the triggering element. Additionally, many older modal patterns use raw `<div>`s for buttons which ignores screen reader expectations.
**Action:** Always store `document.activeElement` before opening a modal and restore focus to it on close. Use semantic `<button>` tags with `aria-label`s for interactive closing actions instead of styled `<div>` elements. Implement Escape key and outside-click listeners for standard UX expectations.

## 2026-04-11 - Scrollable Modal Content Accessibility
**Learning:** When modals contain large amounts of text (like the Sitrep modal), visual users can scroll easily, but keyboard-only users cannot scroll unless the scrollable container itself receives focus. Additionally, without a focus trap, users tabbing through a modal will eventually tab into the hidden background page elements, losing context.
**Action:** Always add `tabindex="0"` to internally scrollable containers so arrow keys work for keyboard users. Implement a simple "focus trap" logic on `keydown` (Tab) inside custom modals to cycle focus between the modal's interactive elements and prevent escaping to the background document.
