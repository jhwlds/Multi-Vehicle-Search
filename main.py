from fastapi import FastAPI
from typing import List

from models import VehicleRequest, SearchResult
from data import LISTINGS_BY_LOCATION
from algorithm import find_cheapest_combination

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Multi-Vehicle Search API"}

@app.post("/", response_model=List[SearchResult])
def search(vehicles: List[VehicleRequest]):
    """Search for locations that can fit all requested vehicles"""
    if not vehicles:
        return []
    
    vehicles_dict = [v.dict() for v in vehicles]
    results = []
    
    for location_id, listings in LISTINGS_BY_LOCATION.items():
        result = find_cheapest_combination(vehicles_dict, listings)
        
        if result:
            listing_ids, total_cost = result
            results.append(SearchResult(
                location_id=location_id,
                listing_ids=listing_ids,
                total_price_in_cents=total_cost
            ))
    
    results.sort(key=lambda x: x.total_price_in_cents)
    
    return results
