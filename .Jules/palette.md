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

## 2026-05-15 - Modal Close Button Polishing and Target Sizes
**Learning:** Even when semantic `<button>` tags are used for modal dismissal, failing to provide adequate click target padding and meaningful visual feedback (hover/focus states) degrades the experience. Furthermore, using a literal "x" character without `aria-hidden="true"` causes screen readers to read "x" redundantly alongside the `aria-label="Close"`, creating noise.
**Action:** Ensure modal close buttons use a larger click area (e.g., `padding: 10px; font-size: 1.5rem`), implement clear `:hover` and `:focus-visible` styles, and utilize the `&times;` entity enclosed in `<span aria-hidden="true">` to prevent screen reader redundancy. Add `title="Close (Esc)"` to provide discoverable keyboard shortcut hints.

## 2026-04-17 - Decorative Emoji Accessibility
**Learning:** Decorative text emojis (like 📍, 🕒, 🌡️, 🤗) behave like raw text to screen readers, causing them to be read aloud (e.g., "round pushpin", "three o'clock") which adds redundant noise to the actual content ("Williamsburg", "15:00 LCL").
**Action:** Always treat decorative text emojis the same as SVG icons. Wrap them in a `<span>` element with `aria-hidden="true"` to prevent screen readers from announcing them, while keeping the visual experience intact.

## 2026-04-18 - Accessible Dynamically Updating Pseudo-Terminals
**Learning:** When building custom interactive terminal or log interfaces, standard input focus doesn't trigger screen readers to announce new lines added to the terminal output container. As a result, users relying on assistive technologies type commands but receive no audio feedback when the terminal responds.
**Action:** Apply `aria-live="polite"` and `aria-atomic="false"` to the container element where dynamic output is appended. This ensures screen readers announce only the new lines as they appear without interrupting the user's typing or reading the entire history.

## 2026-06-12 - Robust Skip-to-Content Links
**Learning:** Adding a "Skip to main content" link is a critical accessibility requirement for keyboard users. To make it robust, it needs to be hidden visually but appear when focused using `transform: translateY(-100%)` instead of magic pixel numbers, and the target container (e.g., `<main>`) must have a matching `id` and `tabindex="-1"` so it can programmatically receive focus across all browsers.
**Action:** Always include a visually hidden 'Skip to main content' link immediately after the opening `<body>` tag. Set the main content container with an `id` and explicitly `tabindex="-1"`.

## 2026-06-25 - Anchor Buttons and Keyboard Accessibility
**Learning:** When using `<a>` tags with `href="#"` as buttons (e.g., to open a modal), native HTML only triggers the `click` event when the user presses `Enter`. However, screen readers and keyboard users expect elements behaving as buttons to also activate on the `Space` key.
**Action:** Add `role="button"` to ensure screen readers announce it properly. Always add a `keydown` event listener that explicitly listens for the `Space` key and prevents the default behavior (page scrolling) to simulate native `<button>` accessibility.
