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

        # Test Skip to main content link
        print("Testing Skip to main content link...")
        await page.goto('http://127.0.0.1:8000/index.html', wait_until='domcontentloaded')

        # Press Tab to focus the first element (should be the skip link)
        await page.keyboard.press('Tab')
        await page.wait_for_timeout(500)

        # Take screenshot of the focused skip link
        await page.screenshot(path="/home/jules/verification/screenshots/skip_link_focused.png")

        # Press Enter to activate skip link and check focus
        await page.keyboard.press('Enter')
        await page.wait_for_timeout(500)

        # Take screenshot after skipping to main content
        await page.screenshot(path="/home/jules/verification/screenshots/main_content_focused.png")

        focused_id = await page.evaluate("document.activeElement.id")
        if focused_id == "main-content":
            print("✅ Skip to main content focus flow verified.")
        else:
            print(f"❌ Failed to verify skip link flow. Active element id: {focused_id}")

        await context.close()
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
