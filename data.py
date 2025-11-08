import json
from collections import defaultdict

def load_listings():
    """Load and group listings by location"""
    with open("listings.json", "r") as f:
        listings = json.load(f)
    
    listings_by_location = defaultdict(list)
    for listing in listings:
        listings_by_location[listing["location_id"]].append(listing)
    
    return listings_by_location

# Load once at module import
LISTINGS_BY_LOCATION = load_listings()

