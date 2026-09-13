import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )

        page = await context.new_page()

        print("Переходим на Ozon (Ноутбуки)...")
        await page.goto("https://www.ozon.by/category/noutbuki-15692/", wait_until="domcontentloaded", timeout=60000)

        await page.wait_for_timeout(5000)

        await page.screenshot(path="ozon_test.png")
        print(f"Заголовок: {await page.title()}")
        print("Скриншот сохранен в ozon_test.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
