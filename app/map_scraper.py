import asyncio, time, random
from playwright.async_api import async_playwright
from app.data_exporters import FileSaver

def search_query(sentence: str):
    return sentence.strip().replace(' ', '+')

async def get_cards(page):
    selectors = [
        "div.Nv2PK",
        "div.CpccDe",
        "div.THOPZb"
    ]

    for selector in selectors:
        cards = await page.query_selector_all(selector)
        if cards:
            return cards
    return []


async def scraper(search:str):

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=100)
        context = await browser.new_context()
        page = await context.new_page()
        search = search_query(search)
        base_url = "https://www.google.com/maps/search/"
        target_url = f"{base_url}{search}hl=en&gl=us"
        
        await page.goto(
            target_url,
            timeout=60000,
            wait_until="domcontentloaded"
        )

        await page.wait_for_timeout(15000)


        last_count = 0
        data = []

        for scroll_count in range(40):
            cards = await get_cards(page)
            count = len(cards)
            print(f"[Scroll {scroll_count}] Found {count} cards so far...")

            if count == last_count:
                print("🛑 No new cards after scrolling. Exiting.")
                break
            last_count = count

            # 👇 this triggers loading
            if cards:
                await cards[-1].scroll_into_view_if_needed()
            random_wait_time = random.uniform(7, 10)
            
            await page.wait_for_timeout(random_wait_time*1000)

        cards = await get_cards(page)
        print(f"✅ Final count: {len(cards)} cards")

        for card in cards:
            anchor = await card.query_selector("a")
            img_el = await card.query_selector("img")
            rating_el = await card.query_selector("span[class*='MW4etd']")
            reviews_el = await card.query_selector("span[class*='UY7F9']")

            name = await anchor.get_attribute("aria-label") if anchor else None
            href = await anchor.get_attribute("href") if anchor else None
            img = await img_el.get_attribute("src") if img_el else None
            rating = await rating_el.text_content() if rating_el else None
            reviews = await reviews_el.text_content() if reviews_el else None

            if name:
                data.append({
                    "name": name,
                    "link": href,
                    "image": img,
                    "rating": rating,
                    "reviews": reviews
                })

        await browser.close()
        return data



