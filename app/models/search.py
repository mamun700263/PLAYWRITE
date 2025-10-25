from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class GoogleMapSearch(BaseModel):
    name: str
    type: Optional[str] = None
    address: Optional[str] = None
    rating: float
    reviews: int
    query: str
    scraped_at: datetime = Field(default_factory=datetime.utcnow)
    link: str
    image: str
