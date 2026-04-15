## 2024-05-24 - Semantic Modals and Focus Styles
**Learning:** In vanilla JavaScript and basic HTML architectures, custom modals frequently lack proper semantic roles (e.g., `role="dialog"`, `aria-modal="true"`) and often misuse `<div>` tags for interactive elements like close buttons, breaking keyboard and screen reader accessibility. Additionally, a global reset often removes default focus outlines, creating navigation issues for keyboard users.
**Action:** Always verify that interactive elements within custom modals use native interactive tags (like `<button>`) with proper `aria-labels`. Ensure dialog containers are announced correctly with ARIA attributes. Implement global `:focus-visible` styles early in the design system to ensure consistent keyboard accessibility without impacting mouse users.

## 2025-05-25 - Semantic HTML Modals and Focus Tracking
**Learning:** Vanilla JS modals often suffer from poor focus management when opened/closed. Users navigating via keyboard get "lost" when a modal closes and their focus is not returned to the triggering element. Additionally, many older modal patterns use raw `<div>`s for buttons which ignores screen reader expectations.
**Action:** Always store `document.activeElement` before opening a modal and restore focus to it on close. Use semantic `<button>` tags with `aria-label`s for interactive closing actions instead of styled `<div>` elements. Implement Escape key and outside-click listeners for standard UX expectations.

## 2026-04-11 - Scrollable Modal Content Accessibility
**Learning:** When modals contain large amounts of text (like the Sitrep modal), visual users can scroll easily, but keyboard-only users cannot scroll unless the scrollable container itself receives focus. Additionally, without a focus trap, users tabbing through a modal will eventually tab into the hidden background page elements, losing context.
**Action:** Always add `tabindex="0"` to internally scrollable containers so arrow keys work for keyboard users. Implement a simple "focus trap" logic on `keydown` (Tab) inside custom modals to cycle focus between the modal's interactive elements and prevent escaping to the background document.

## 2026-04-12 - Loading States for Async Widgets
**Learning:** The local-info widget fetches IP and weather data asynchronously. Without a loading state, the UI container pops into existence or stays empty, which looks janky or broken to users on slow connections. When errors occur, silent failures leave the user wondering if the widget is broken.
**Action:** Always provide immediate visual feedback (like a loading message or skeleton state) when initiating an async fetch that updates the UI. If the fetch fails, show a graceful error state rather than failing silently or leaving the UI blank. Ensure icons used in states have `aria-hidden="true"`.

## 2024-05-26 - Modal Close Button Accessibility and Click Targets
**Learning:** Decorative text characters like 'x' used for close buttons are often announced by screen readers alongside the `aria-label`, creating redundant noise (e.g., "Close, x, button"). Additionally, inline styles stripping padding from these buttons severely reduce the click target size, making them difficult to use, and a lack of hover/focus styles makes discoverability poor for sighted keyboard users.
**Action:** Always wrap visual close characters (like `&times;`) in `<span aria-hidden="true">` to hide them from screen readers when an `aria-label` is present. Move button styling to CSS to ensure adequate padding for click targets, and always define explicit `:hover` and `:focus-visible` states. Use a `title` attribute (e.g., `title="Close (Esc)"`) to hint at available keyboard shortcuts.
