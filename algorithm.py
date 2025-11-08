from typing import List, Dict, Tuple, Optional
from itertools import combinations

def can_fit_vehicles(vehicles: List[Dict], listing_length: int, listing_width: int) -> bool:
    """Check if vehicles can fit in given space (try both orientations)"""
    expanded = []
    for v in vehicles:
        for _ in range(v["quantity"]):
            expanded.append(v["length"])
    
    total_length = sum(expanded)
    
    # Orientation 1: vehicles placed along length
    if total_length <= listing_length and 10 <= listing_width:
        return True
    
    # Orientation 2: vehicles placed along width
    if total_length <= listing_width and 10 <= listing_length:
        return True
    
    return False

def can_allocate(vehicles: List[int], listings: List[Dict]) -> bool:
    """Check if vehicles can be allocated to listings using backtracking"""
    if not vehicles:
        return True
    
    # Create list of available spaces (two orientations per listing)
    spaces = []
    for listing in listings:
        spaces.append([listing["length"], listing["width"]])
        spaces.append([listing["width"], listing["length"]])
    
    def backtrack(idx: int, spaces: List[List[int]]) -> bool:
        if idx == len(vehicles):
            return True
        
        vehicle_len = vehicles[idx]
        
        for i, space in enumerate(spaces):
            if vehicle_len <= space[0] and 10 <= space[1]:
                new_spaces = [s[:] for s in spaces]
                new_spaces[i][0] -= vehicle_len
                
                if backtrack(idx + 1, new_spaces):
                    return True
        
        return False
    
    return backtrack(0, spaces)

def find_cheapest_combination(vehicles: List[Dict], listings: List[Dict]) -> Optional[Tuple[List[str], int]]:
    """Find the cheapest combination of listings that fits all vehicles"""
    sorted_listings = sorted(listings, key=lambda x: x["price_in_cents"])
    
    vehicle_lengths = []
    for v in vehicles:
        for _ in range(v["quantity"]):
            vehicle_lengths.append(v["length"])
    
    # Try single listing first
    for listing in sorted_listings:
        if can_fit_vehicles(vehicles, listing["length"], listing["width"]):
            return [listing["id"]], listing["price_in_cents"]
    
    # Try combinations of increasing size
    max_combo_size = min(len(sorted_listings), 5)
    
    for size in range(2, max_combo_size + 1):
        best_cost = float('inf')
        best_combo = None
        
        for combo in combinations(sorted_listings, size):
            total_cost = sum(l["price_in_cents"] for l in combo)
            
            if total_cost >= best_cost:
                continue
            
            if can_allocate(vehicle_lengths, list(combo)):
                best_cost = total_cost
                best_combo = [l["id"] for l in combo]
        
        if best_combo:
            return best_combo, best_cost
    
    return None

