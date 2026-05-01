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

## 2026-05-19 - Skip Links and Keyboard Focus Consistency
**Learning:** Skip links are essential for keyboard users to bypass repetitive navigation elements, but simply hiding them visually using absolute positioning off-screen (e.g., `top: -40px`) can be fragile across different screen sizes, font sizes, or zoom levels. Furthermore, linking to a main container that lacks `tabindex="-1"` fails to programmatically focus the container in some browsers, breaking the navigation flow.
**Action:** Always include a visually hidden 'Skip to main content' link immediately after the opening `<body>` tag. Use `transform: translateY(-100%)` for robust hiding and display it on `:focus` using `transform: translateY(0)`. Ensure the main content container has a matching `id` attribute and explicitly set `tabindex="-1"` so it can consistently receive programmatic focus across all browsers.
