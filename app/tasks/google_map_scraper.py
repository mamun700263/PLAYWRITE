from app.core import Logger
from app.core.data_exporters import FileSaver
from app.google_map.scraper import scraper
from app.core.celery import celery_app

logger = Logger.get_logger(__file__,'google_map')
@celery_app.task(bind=True,name="map scraper")
def run_scraper(self,query: str, file_name: str):
    logger.info(f"started search for : {query} and file saving as {file_name}")
    try:
        logger.info(f"Starting scrape for: {query}")
        data =scraper(query)
        FileSaver.save(data, f"{file_name}")
        logger.info(f"[SUCCESS] Saved results to {file_name}")
        return data
    except Exception as e:
        self.retry(exc=e, countdown=5, max_retries=3)

