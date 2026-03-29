from playwright.sync_api import sync_playwright

def run_cuj(page):
    page.goto("http://localhost:8000/index.html")
    page.wait_for_timeout(500)
    page.screenshot(path="/home/jules/verification/screenshots/index_with_nav.png")
    page.wait_for_timeout(500)
    page.get_by_text("Contact").click()
    page.wait_for_timeout(500)
    page.screenshot(path="/home/jules/verification/screenshots/contact_page.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
