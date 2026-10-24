from playwright.async_api import async_playwright
import asyncio
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        print("dar hale baz kardan site")
        await page.goto("http://quotes.toscrape.com/js/")
        await page.wait_for_selector(".quote",timeout=10000)
        quote = await page.locator(".quote.txt").all_text_contents()
        print(f"\ntedad quote haye peyda shode : {len(quote)}")
        for p in quote:
            print(quote)
        await browser.close()
asyncio.run(main())