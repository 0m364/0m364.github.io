import asyncio
from playwright.async_api import async_playwright
import time
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--font-render-hinting=none',
                '--disable-features=IsolateOrigins,site-per-process'
            ]
        )
        context = await browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = await context.new_page()

        print("Testing loading and error states...")

        # Test Error State (block network requests to force error)
        await page.route("**/*", lambda route: route.abort() if route.request.url.startswith("https://get.geojs.io") or route.request.url.startswith("https://api.open-meteo.com") else route.continue_())

        # Clear localStorage cache
        await page.goto('http://127.0.0.1:8000/contact.html', wait_until='domcontentloaded')
        await page.evaluate("localStorage.clear();")
        await page.wait_for_timeout(500)

        await page.goto('http://127.0.0.1:8000/contact.html', wait_until='domcontentloaded')

        # We expect to see the error message
        try:
            await page.wait_for_selector('text=Telemetry currently unavailable', timeout=3000)
            print("✅ Error state verified.")
        except Exception as e:
            print("❌ Failed to verify error state.", e)

        await page.screenshot(path="/home/jules/verification/screenshots/error_state.png")
        await page.wait_for_timeout(1000)

        print("Testing skip link accessibility...")
        await page.goto('http://127.0.0.1:8000/index.html', wait_until='domcontentloaded')

        try:
            # Press Tab to focus the skip link
            await page.keyboard.press('Tab')

            # Check if it has focus
            is_focused = await page.evaluate("document.activeElement.classList.contains('skip-link')")
            if is_focused:
                print("✅ Skip link received focus.")
                await page.screenshot(path="/home/jules/verification/screenshots/skip_link_focused.png")
            else:
                print("❌ Skip link did not receive focus.")

            # Press Enter to follow the link
            await page.keyboard.press('Enter')
            await page.wait_for_timeout(500)

            # Check if focus moved to main content
            active_id = await page.evaluate("document.activeElement.id")
            # Usually jumping to a hash anchor makes the target element the :target, but may not shift activeElement unless it has tabindex="-1".
            # Let's check the hash.
            current_hash = await page.evaluate("window.location.hash")
            if current_hash == "#main-content":
                 print("✅ Hash updated to #main-content.")
            else:
                 print("❌ Hash not updated.")

        except Exception as e:
            print("❌ Failed to verify skip link.", e)

        await context.close()
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
