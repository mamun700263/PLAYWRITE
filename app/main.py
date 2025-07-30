import asyncio
from .map_scraper import scraper
from app.data_exporters import FileSaver

query = input("search -> ")
file_name = input("what would be the file name? ")


x = asyncio.run(scraper(query))
FileSaver.save(x,f'{file_name}')