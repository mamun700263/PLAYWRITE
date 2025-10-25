import asyncio
import os
from core.data_exporters import FileSaver
from app.google_map.scraper import scraper


async def run_scraper(query: str, file_name: str):
    print(f"[INFO] Starting scrape for: {query}")
    data = await scraper(query)
    FileSaver.save(data, f"{file_name}")
    print(f"[SUCCESS] Saved results to {file_name}")


if __name__ == "__main__":
    # Non-interactive defaults (for Docker)
    query = os.getenv("QUERY")
    file_name = os.getenv("FILENAME")

    if not query or not file_name:
        # fallback to interactive mode
        query = input("search -> ").strip()
        file_name = input("what would be the file name? ").strip()
        FileSaver.check_format(file_name)
    asyncio.run(run_scraper(query, file_name))

# shops that are open
# distance
# python3 runner.py
# burger shops near me
# burger.json
