## 2024-05-24 - Semantic Modals and Focus Styles
**Learning:** In vanilla JavaScript and basic HTML architectures, custom modals frequently lack proper semantic roles (e.g., `role="dialog"`, `aria-modal="true"`) and often misuse `<div>` tags for interactive elements like close buttons, breaking keyboard and screen reader accessibility. Additionally, a global reset often removes default focus outlines, creating navigation issues for keyboard users.
**Action:** Always verify that interactive elements within custom modals use native interactive tags (like `<button>`) with proper `aria-labels`. Ensure dialog containers are announced correctly with ARIA attributes. Implement global `:focus-visible` styles early in the design system to ensure consistent keyboard accessibility without impacting mouse users.

## 2025-05-25 - Semantic HTML Modals and Focus Tracking
**Learning:** Vanilla JS modals often suffer from poor focus management when opened/closed. Users navigating via keyboard get "lost" when a modal closes and their focus is not returned to the triggering element. Additionally, many older modal patterns use raw `<div>`s for buttons which ignores screen reader expectations.
**Action:** Always store `document.activeElement` before opening a modal and restore focus to it on close. Use semantic `<button>` tags with `aria-label`s for interactive closing actions instead of styled `<div>` elements. Implement Escape key and outside-click listeners for standard UX expectations.

## 2025-05-25 - Contrast Ratios and Decorative SVGs
**Learning:** Light-on-light theme defaults (e.g. #d3d3d3 on #85c1e9) often sneak into generic CSS button classes causing severe WCAG contrast failures (1.30:1). Similarly, inline decorative SVGs within links or buttons without `aria-hidden="true"` create redundant noise for screen reader users.
**Action:** Always verify contrast ratios for dynamic button states (active/hover) against WCAG AA (4.5:1). Apply `color: #000000` (or appropriate high-contrast foreground) on light backgrounds. Ensure all purely decorative SVGs contain `aria-hidden="true"`.
