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

        print("Загружаем страницу каталога...", flush=True)
        await page.goto("https://www.ozon.by/category/noutbuki-15692/", wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(timeout=3000)
        print("Прокручиваем страницу...", flush=True)
        for _ in range(6):
            await page.mouse.wheel(0,1200)
            await page.wait_for_timeout(timeout=1000)

        links = await page.eval_on_selector_all(
            'a[href*="/product/"]',
            'elements => elements.map(e => e.href)'
        )

        unique_links = list(set(links))

        print(f"Успешно найдено уникальных ссылок: {len(unique_links)}", flush=True)

        with open("links.txt", "w", encoding="utf-8") as f:
            for link in unique_links:
                f.write(f"{link}\n")

        print("Ссылки сохранены в links.txt", flush=True)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())