import asyncio
import json
import random
from playwright.async_api import async_playwright
import re

async def handle_captcha(page):
    captcha_locator = page.locator('text="Сопоставьте пазл"')
    if await captcha_locator.count() > 0:
        print("\n CAPTCHA ALARM CAPTCHA ALARM CAPTCHA ALARM CAPTCHA ALARM CAPTCHA ALARM")
        for _ in range(45):
            await page.wait_for_timeout(1000)
            if await captcha_locator.count() == 0:
                print("Капча решена! Продолжаем парсинг...\n", flush=True)
                await page.wait_for_timeout(2000)
                return True
            print("Капча не решена вовремя", flush=True)
            return False
    return True

async def parse_laptop(page,url: str):
    try:
        await page.goto(url,
                        referer="https://www.ozon.by/category/noutbuki-15692/",
                        wait_until="domcontentloaded",
                        timeout=60000
                        )
        await page.wait_for_timeout(2500)
        if not await handle_captcha(page):
            return None

        if await page.locator('text="Похоже, нет соединения"').count() > 0:
            print(" Поймали заглушку соединения. Пробуем обновить страницу...", flush=True)
            await page.reload(wait_until="domcontentloaded")
            await(page.wait_for_timeout(3000))
        title_element = page.locator('h1')
        title = await title_element.text_content() if await title_element.count() > 0 else None

        price = None
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
                    price = None

        return {"url":url,
                "title":title.strip() if title else None,
                "price_byn":price}
    except Exception as e:
        print(f"Ошибка при обработке ссылки {url}: {e}", flush=True)
        return None

async def main():
    with open("links.txt", "r", encoding="utf-8") as f:
        links = [line.strip() for line in f if line.strip()]

    total = len(links)
    print(f"Запуск сбора данных. Всего ссылок: {total}\n", flush=True)

    results = []

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else await context.new_page()

        print("Начинаем сбор товаров... \n",flush=True)

        for idx,link in enumerate(links,1):
            print(f"[{idx}/{total}] Парсим карточку...",flush=True)
            data = await parse_laptop(page,link)

            if data and data.get("title"):
                results.append(data)
                safe_title = (data['title'] or "Без названия")[:40]
                print(f"   -> Успешно: {safe_title}... | Цена: {data['price_byn']} BYN", flush=True)
            else:
                print("   -> Пропущено / не удалось собрать данные", flush=True)
            delay = random.uniform(4.0,7.0)
            await asyncio.sleep(delay)


    with open("laptops_data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print(f"\n Готово! Собрано объектов: {len(results)} из {total}")
    print("Данные сохранены в файл laptops_data.json")

    try:
        await context.close()
    except Exception:
        pass


if __name__ == "__main__":
    asyncio.run(main())