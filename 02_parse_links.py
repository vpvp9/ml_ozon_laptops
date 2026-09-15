import asyncio
import random
from playwright.async_api import async_playwright

BASE_URL = "https://www.ozon.by/category/noutbuki-15692/?page="
PAGES_TO_PARSE = 20

async def main():
    all_links = set()
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else await context.new_page()

        print(f"Начинаем сбор ссылок с {PAGES_TO_PARSE} страниц каталога...\n")

        for page_num in range(1, PAGES_TO_PARSE + 1):
            url = f"{BASE_URL}{page_num}"
            print(f"[Страница {page_num}/{PAGES_TO_PARSE}] Переходим на {url}...")

            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(random.uniform(3.0,5.0))

            for _ in range(4):
                await page.evaluate("window.scrollBy(0, 1000)")
                await asyncio.sleep(random.uniform(0.9,1.3))

            links_elements = await page.locator('a[href*="/product/"]').all()
            page_links = 0

            for elem in links_elements:
                href = await elem.get_attribute("href")
                if href and "/product/" in href:
                    clean_url = "https://www.ozon.by" + href.split("?")[0]
                    if clean_url not in all_links:
                        all_links.add(clean_url)
                        page_links += 1

            print(f"   -> Найдено новых ссылок на странице: {page_links} | Всего: {len(all_links)}")

    with open("links.txt","w",encoding="utf-8") as f:
        for link in all_links:
            f.write(f"{link}\n")

    print(f"Готово! Собрано уникальных ссылок: {len(all_links)}")
    print("Ссылки обновлены в файле links.txt")

if __name__ == "__main__":
    asyncio.run(main())