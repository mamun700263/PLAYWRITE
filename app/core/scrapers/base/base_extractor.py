from bs4 import BeautifulSoup, Tag

from typing import List, Dict

from ...logger import Logger


class BaseProductExtractor:
    def __init__(self, soup: BeautifulSoup, base_url: str, logger: Logger):
        self.soup = soup
        self.base_url = base_url
        self.logger = logger

    def list_items(self) -> List[Tag]:
        """Locate all product list items from the soup."""
        try:
            items = self.soup.select('div[role="listitem"]') or []
            self.logger.info(f"✅ Found {len(items)} product items")
            return items
        except Exception as e:
            self.logger.error(f"❌ Error locating list items: {e}")
            return []

    @staticmethod
    def extract_text(item: Tag, selector: str, logger: Logger, attr: str = None) -> str:
        """Extract text or attribute value from an HTML element."""
        try:
            element = item.find(selector) or ""
            return element.get(attr) if attr else element.text.strip()
        except Exception as e:
            logger.warning(f"⚠️ Extraction failed for selector '{selector}': {e}")
            return ""

    def extract_field(self, item: Tag, field_type: str) -> str:
        """Extract specific field (title, image, link) from product item."""
        field_selectors = {"title": "h2", "image": "img", "link": "a"}

        attrs = {
            "image": "src",
            "link": "href",
        }

        selector = field_selectors.get(field_type)
        attr = attrs.get(field_type)  # Will be None for title

        if not selector:
            self.logger.warning(f"⚠️ Unknown field type: {field_type}")
            return ""

        extracted = self.extract_text(item, selector, self.logger, attr)

        if field_type == "link" and extracted:
            return f"{self.base_url}{extracted}"
        return extracted

    def extract(self) -> List[Dict[str, str]]:
        """Main extraction logic."""
        if not self.soup:
            self.logger.error("❌ No soup provided to extractor")
            return []

        items = self.list_items()
        results = []

        for item in items:
            title = self.extract_field(item, "title")
            if not title:
                continue  # Skip items with no title

            product = {
                "Title": title,
                "Image": self.extract_field(item, "image"),
                "Link": self.extract_field(item, "link"),
            }
            self.logger.debug(f"📝 Product extracted: {title}")
            results.append(product)

        self.logger.info(f"✅ Extracted {len(results)} products successfully")
        return results
