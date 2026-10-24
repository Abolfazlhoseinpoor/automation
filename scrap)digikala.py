import asyncio
import re
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

    
        await page.goto("https://www.digikala.com/search/?q=iphone")
        import re



        async def run(playwright: Playwright) -> None:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto("https://www.digikala.com/search/?q=iphone")
            page.get_by_role("link").filter(has_text="غیراصلبرچسب پوششی مدل E11").click()
            page.locator("div").filter(has_text=re.compile(r"^۵۰۰,۰۰۰$")).nth(2).click()
            page.locator("div").filter(has_text=re.compile(r"^برچسب پوششی مدل E11 مناسب برای گوشی موبایل اپل Iphone X/XS$")).click()
            page.get_by_text("(امتیاز ۷۸ خریدار)").click()
            page.get_by_role("button", name="مشاهده همه ویژگی‌ها").click()
            page.get_by_text("مشخصاتسازگار با گوشی موبایل").click()

            await page.wait_for_selector("div[data-testid='product-card']", timeout=15000)
            cards = await page.locator("div[data-testid='product-card']").all()
            print(f"تعداد محصولات: {len(cards)}")


        for i, card in enumerate(cards[:3]):
            full_text = await card.text_content()
            title = await card.locator("h3").first.text_content()
            
            price = "قیمت پیدا نشد"
            if "تومان" in full_text:
                parts = full_text.split("تومان")
                raw_price = parts[0].strip().split()[-1] 
                price = raw_price + " تومان"

            print(f"\nمحصول {i+1}:")
            print(f"عنوان: {title.strip()}")
            print(f"قیمت: {price}")
            
        await browser.close()

asyncio.run(main())