from playwright.async_api import async_playwright
import asyncio

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        print("Dar hale baz kardan site...")
        await page.goto("http://quotes.toscrape.com/js/")
 
        await page.wait_for_selector(".quote", timeout=10000)
        quotes_page1 = await page.locator(".quote .text").all_text_contents()
        
        print(f"\n--- Safhe 1 ---")
        print(f"Tedad quote: {len(quotes_page1)}")
        for q in quotes_page1:
            print(f"- {q}")

        print("\nDar hale raftan be safhe 2...")
        await page.click("li.next a") 
        
        await page.wait_for_timeout(2000) 

        quotes_page2 = await page.locator(".quote .text").all_text_contents()
        
        print(f"\n--- Safhe 2 ---")
        print(f"Tedad quote: {len(quotes_page2)}")
        for q in quotes_page2:
            print(f"- {q}")
            
        await browser.close()
        print("\nMarvargar baste shod.")

asyncio.run(main())