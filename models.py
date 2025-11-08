from pydantic import BaseModel
from typing import List

class VehicleRequest(BaseModel):
    length: int
    quantity: int

class SearchResult(BaseModel):
    location_id: str
    listing_ids: List[str]
    total_price_in_cents: int

