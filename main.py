from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json
import os

app = FastAPI()

class VehicleRequest(BaseModel):
    length: int
    quantity: int


class SearchResult(BaseModel):
    location_id: str
    listing_ids: List[str]
    total_price_in_cents: int

LISTINGS_PATH = os.path.join(os.path.dirname(__file__), "listings.json")

with open(LISTINGS_PATH, "r") as f:
    LISTINGS = json.load(f)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Multi-Vehicle-Search API is running"}
    
@app.post("/search", response_model=List[SearchResult])
def search(vehicles: List[VehicleRequest]):

    if not LISTINGS:
        return []

    results: List[SearchResult] = []

    cheapest_by_location = {}
    for listing in LISTINGS:
        loc_id = listing["location_id"]
        price = listing["price_in_cents"]
        if loc_id not in cheapest_by_location or price < cheapest_by_location[loc_id]["price_in_cents"]:
            cheapest_by_location[loc_id] = listing

    for loc_id, listing in list(cheapest_by_location.items())[:5]:
        result = SearchResult(
            location_id=loc_id,
            listing_ids=[listing["id"]],
            total_price_in_cents=listing["price_in_cents"]
        )
        results.append(result)

    return results