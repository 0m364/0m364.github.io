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

        # Test Modal Keyboard Accessibility (Space key)
        print("Testing modal keyboard accessibility...")
        await page.goto('http://127.0.0.1:8000/concepts.html', wait_until='domcontentloaded')
        try:
            btn = page.locator('#sitrep-btn')
            await btn.focus()
            await btn.press('Space')
            await page.wait_for_selector('#sitrep-modal', state='visible', timeout=2000)
            print("✅ Modal keyboard accessibility (Space) verified.")
            await page.screenshot(path="/home/jules/verification/screenshots/modal_opened_space.png")
        except Exception as e:
            print("❌ Failed to verify modal keyboard accessibility.", e)

        await context.close()
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
