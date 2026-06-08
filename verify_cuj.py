from playwright.sync_api import sync_playwright

def run_cuj(page):
    page.goto("http://localhost:8000/products.html")
    page.wait_for_timeout(500)

    # Focus the sitrep button
    page.locator('#sitrep-btn').focus()
    page.wait_for_timeout(500)

    # Press space to open modal
    page.keyboard.press("Space")
    page.wait_for_timeout(500)

    # Take screenshot of the open modal
    page.screenshot(path="/home/jules/verification/screenshots/verification.png")
    page.wait_for_timeout(1000)

    # Close modal
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--font-render-hinting=none',
                '--disable-features=IsolateOrigins,site-per-process'
            ]
        )
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
