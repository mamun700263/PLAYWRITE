from app.models import GoogleMapSearch


async def extract_card(card: str):
    anchor = await card.query_selector("a")
    img_el = await card.query_selector("img")
    rating_el = await card.query_selector("span[class*='MW4etd']")
    reviews_el = await card.query_selector("span[class*='UY7F9']")
    spans = await card.query_selector_all("div.UaQhfb div.W4Efsd div.W4Efsd span")
    type_of_place = await spans[0].text_content()

    # print(len(spans))
    # x = 0
    # for i in spans:
    #     t = await i.text_content()
    #     print(x, t)
    #     x += 1
    # print(t)

    if spans:
        try:
            address = await spans[6].text_content()
            # if address.size() < 2:
            #     address = await spans[6].text_content()
            # else:
            #     address = await spans.text_content()
        except:
            address = None
    else:
        address = None

    name = await anchor.get_attribute("aria-label") if anchor else None
    href = await anchor.get_attribute("href") if anchor else None
    img = await img_el.get_attribute("src") if img_el else None
    rating = await rating_el.text_content() if rating_el else None
    reviews = await reviews_el.text_content() if reviews_el else None
    price_rage = ""
    status = ""

    return GoogleMapSearch(
        **{
            "name": name,
            "type": type_of_place,
            "address": address,
            "link": href,
            "image": img,
            "rating": rating,
            "reviews": reviews,
            "query": "n/a",
        }
    )


async def get_cards(page, logger):
    selectors = ["div.Nv2PK", "div.CpccDe", "div.THOPZb"]

    for selector in selectors:
        cards = await page.query_selector_all(selector)
        logger.info(f"found {len(cards)} cards with selecor {selector}")
        if cards:
            return cards
    return []
