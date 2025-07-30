from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        slow_mo=50,
        args=["--start-maximized"]
    )
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},  # 🧠 Force full screen size
        screen={"width": 1920, "height": 1080}
    )
    page = context.new_page()

    page.goto("https://www.google.com/maps/search/schools+in+dhanmondi?")
    # Maximize the container scroll to get more cards loaded
    container_selector = 'div.m6QErb.WNBkOb.XiKgde[role="main"]'

    last_count = 0

    for _ in range(30):
        cards = page.query_selector_all("div.Nv2PK.THOPZb.CpccDe")
        count = len(cards)

        if count == last_count:
            break  # No more new cards

        last_count = count

        page.eval_on_selector(
            container_selector,
            "(el) => el.scrollBy(0, el.clientHeight)"
        )

        page.wait_for_timeout(1000)  # wait for more cards to load

    page.pause()

