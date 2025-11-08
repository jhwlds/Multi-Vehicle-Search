from typing import List, Dict, Tuple, Optional
from itertools import combinations

def can_fit_vehicles(vehicles: List[Dict], listing_length: int, listing_width: int) -> bool:
    """Check if vehicles can fit in given space with 2D grid packing
    All vehicles must face the same direction within a listing"""

    # Expand all vehicle lengths into a flat list
    lengths: List[int] = []
    for v in vehicles:
        for _ in range(v["quantity"]):
            lengths.append(v["length"])

    if not lengths:
        return True  # No vehicles, always fits

    # Sort by length descending for better pruning
    lengths.sort(reverse=True)

    def can_fit_orientation(L: int, W: int) -> bool:
        """
        Check if vehicles can fit when their length goes along L direction
        with rows of width 10 stacked within W
        - Number of rows = W // 10
        - Capacity of each row = L
        """
        rows_count = W // 10
        if rows_count == 0:
            return False  # Width less than 10, no vehicle can fit

        # Remaining space in each row [L, L, L, ...]
        rows = [L] * rows_count
        n = len(lengths)

        # Backtracking: place i-th vehicle into rows
        def backtrack(i: int) -> bool:
            if i == n:
                return True  # All vehicles placed

            v_len = lengths[i]
            seen = set()  # Avoid duplicate attempts on rows with same remaining space (pruning)

            for r in range(rows_count):
                if rows[r] >= v_len and rows[r] not in seen:
                    seen.add(rows[r])

                    rows[r] -= v_len
                    if backtrack(i + 1):
                        return True
                    rows[r] += v_len  # Backtrack

            return False  # Cannot fit in any row

        return backtrack(0)

    # Orientation 1: vehicle length along listing length
    if can_fit_orientation(listing_length, listing_width):
        return True

    # Orientation 2: vehicle length along listing width (90 degree rotation)
    if can_fit_orientation(listing_width, listing_length):
        return True

    return False


def can_allocate(vehicles: List[int], listings: List[Dict]) -> bool:
    """Allocate vehicles to multiple listings with 2D packing in each listing"""
    if not vehicles:
        return True
    
    n_vehicles = len(vehicles)
    n_listings = len(listings)
    
    # Sort vehicles for better pruning
    vehicles = sorted(vehicles, reverse=True)
    
    # Try to distribute vehicles across listings
    def backtrack(v_idx: int, listing_allocations: List[List[int]]) -> bool:
        """
        v_idx: current vehicle index
        listing_allocations: list of lists, each containing vehicle lengths assigned to that listing
        """
        if v_idx == n_vehicles:
            # All vehicles allocated, now check if each listing can fit its vehicles in 2D
            for i, allocated_vehicles in enumerate(listing_allocations):
                if allocated_vehicles:
                    # Convert to the format can_fit_vehicles expects
                    vehicles_dict = [{"length": v, "quantity": 1} for v in allocated_vehicles]
                    if not can_fit_vehicles(vehicles_dict, listings[i]["length"], listings[i]["width"]):
                        return False
            return True
        
        vehicle_len = vehicles[v_idx]
        
        # Try placing current vehicle in each listing
        for listing_idx in range(n_listings):
            listing_allocations[listing_idx].append(vehicle_len)
            
            if backtrack(v_idx + 1, listing_allocations):
                return True
            
            listing_allocations[listing_idx].pop()
        
        return False
    
    # Initialize empty allocation for each listing
    listing_allocations = [[] for _ in range(n_listings)]
    
    return backtrack(0, listing_allocations)


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
