import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('http://localhost:8000/contact.html')
        await page.screenshot(path='contact_page_new_qr_python.png', full_page=True)
        await browser.close()

asyncio.run(main())
