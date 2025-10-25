from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseScraper(ABC):
    """
    Base class for all scrapers.
    Every custom scraper (Amazon, Flipkart, etc.) should inherit from this.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Set up the scraper with custom config, if any.
        e.g. headers, proxies, cookies, search query, etc.
        """
        self.config = config or {}

    @abstractmethod
    def fetch(self) -> Any:
        """
        Fetch raw HTML/data from target source (requests or selenium).
        """
        pass

    @abstractmethod
    def parse(self, raw_data: Any) -> List[Dict[str, Any]]:
        """
        Parse the raw data into structured format (dicts/lists).
        """
        pass

    def scrape(self) -> List[Dict[str, Any]]:
        """
        Full scrape pipeline = fetch → parse.
        Can be overridden for custom pipelines.
        """
        raw_data = self.fetch()
        return self.parse(raw_data)
