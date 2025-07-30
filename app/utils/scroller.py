import time
from .logger import Logger

logger = Logger.get_logger()
class Scroller:
    @staticmethod
    def get_scroll_height(driver, selector) -> int:
        return driver.execute_script(f"return document.querySelector('{selector}').scrollHeight")

    @staticmethod
    def scroll_and_wait(driver, selector, wait_time=2, scroll_pause=1.5, max_scrolls=15):
        last_height = Scroller.get_scroll_height(driver, selector)

        for i in range(max_scrolls):
            driver.execute_script(
                f"document.querySelector('{selector}').scrollBy(0, document.querySelector('{selector}').clientHeight);"
            )
            time.sleep(scroll_pause)
            new_height = Scroller.get_scroll_height(driver, selector)

            logger.debug(f"🔁 Scroll {i+1}: {last_height} → {new_height}")
            if new_height == last_height:
                logger.info("📉 No new content loaded — stopping scroll")
                break
            last_height = new_height

        logger.info(f"✅ Scrolling completed with {i+1} scroll(s)")
        time.sleep(wait_time)
