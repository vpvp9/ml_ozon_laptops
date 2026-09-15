import asyncio
from playwright.async_api import async_playwright
import re

async def parse_single_laptop(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = await context.new_page()

        print(f"Открваем карточку: {url}", flush=True)
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(4000)

        title_element = page.locator('h1')
        title = await title_element.text_content() if await title_element.count() > 0 else "Не найдено"

        price = "Не найдена"
        price_widget = page.locator('[data-widget="webPrice"]')

        if await price_widget.count()>0:
            price_text = await price_widget.text_content()
            match = re.search(r'([\d\s\xa0,]+)\s*(р\.|руб|BYN)', price_text)
            if match:
                raw_price = match.group(1)
                clean_price = re.sub(r'[\s\xa0]','',raw_price).replace(',','.')
                try:
                    price = float(clean_price)
                except ValueError:
                    price = clean_price

        print("\n---Собрано---")
        print(f"Название: {title.strip()}")
        print(f"Цена: {price}")
        print("----------------\n")

        await browser.close()

async def main():
    with open("links.txt", "r", encoding="utf-8") as f:
        first_link = f.readline().strip()

    if first_link:
        await parse_single_laptop(first_link)

if __name__ == "__main__":
    asyncio.run(main())

